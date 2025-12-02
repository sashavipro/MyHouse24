"""src/finance/tasks.py."""

import io
import logging

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMessage
from weasyprint import HTML
from xlsx2html import xlsx2html

from src.core.utils import ReceiptExcelGenerator
from src.finance.models import PrintTemplate
from src.finance.models import Receipt

logger = logging.getLogger(__name__)


@shared_task
def send_receipt_email_task(receipt_id, template_id=None):
    """Generate PDF receipts and sends them to the owner's email address."""
    try:
        receipt = Receipt.objects.select_related(
            "apartment__owner", "apartment__house"
        ).get(pk=receipt_id)

        owner = receipt.apartment.owner
        if not owner or not owner.email:
            logger.warning(
                "У владельца квартиры для квитанции %s нет Email.",  # noqa: RUF001
                receipt.number,
            )
            return "Email not set for owner"

        if template_id:
            template = PrintTemplate.objects.get(pk=template_id)
        else:
            template = PrintTemplate.objects.filter(is_default=True).first()
            if not template:
                template = PrintTemplate.objects.first()

        if not template:
            logger.error("Не найден шаблон для печати квитанции.")  # noqa: RUF001
            return "Template not found"

        generator = ReceiptExcelGenerator(receipt, template.template_file.path)
        workbook = generator.generate_workbook()

        excel_buffer = io.BytesIO()
        workbook.save(excel_buffer)
        excel_buffer.seek(0)

        html_buffer = io.StringIO()
        xlsx2html(excel_buffer, html_buffer)
        raw_html = html_buffer.getvalue()

        # CSS для PDF
        custom_css = """
        <style>
            @page { size: 250mm 300mm; margin: 0; }
            body { margin: 10mm; padding: 0; font-family: sans-serif; }
            table { border-collapse: collapse; border-spacing: 0; width: 100%; }
            tr[height="0"], tr[style*="height:0"] { display: none !important; }
        </style>
        """
        final_html_content = custom_css + raw_html

        base_url = getattr(settings, "SITE_URL", "http://localhost:8000")

        pdf_file = HTML(string=final_html_content, base_url=base_url).write_pdf()

        subject = f"Квитанция на оплату №{receipt.number}"
        body = (
            f"Здравствуйте, {owner.get_full_name()}!\n\n"
            f"Направляем вам квитанцию на оплату коммунальных услуг.\n"
            f"Квартира: {receipt.apartment.number}, "
            f"Дом: {receipt.apartment.house.title}.\n\n"
            f"С уважением,\nАдминистрация."  # noqa: RUF001
        )

        email = EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.EMAIL_HOST_USER,
            to=[owner.email],
        )

        filename = f"receipt_{receipt.number}.pdf"
        email.attach(filename, pdf_file, "application/pdf")

        email.send(fail_silently=False)
        logger.info(
            "Квитанция %s успешно отправлена на %s", receipt.number, owner.email
        )

    except (Receipt.DoesNotExist, PrintTemplate.DoesNotExist):
        logger.exception("Объект не найден для отправки квитанции ID %s", receipt_id)
        return "Object not found"
    except Exception as e:
        logger.exception("Ошибка при отправке квитанции %s", receipt_id)
        return f"Error: {e}"
    else:
        return "Sent"
