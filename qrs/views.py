import qrcode
from io import BytesIO
from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from django.http import HttpResponse, FileResponse
from .models import QRCode
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from django.conf import settings
import mimetypes
from django.contrib import messages
import os

def crear_qr(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        url = request.POST['url']

        qr_obj = QRCode.objects.create(nombre=nombre, url_destino=url)
        url_redir = request.build_absolute_uri(f'/v/{qr_obj.id}/')

        qr_img = qrcode.make(url_redir)
        buffer = BytesIO()
        qr_img.save(buffer)
        filename = f'{nombre}.png'
        qr_obj.imagen_qr.save(filename, ContentFile(buffer.getvalue()))
        qr_obj.save()

        return redirect('listar_qrs')
    return render(request, 'crear_qr.html')


def ver_qr(request, qr_id):
    qr = get_object_or_404(QRCode, id=qr_id)
    qr.visitas += 1
    qr.save()
    return redirect(qr.url_destino)


def listar_qrs(request):
    qrs = QRCode.objects.all()
    return render(request, 'listar_qrs.html', {'qrs': qrs})


def descargar_qr_imagen(request, qr_id):
    qr = get_object_or_404(QRCode, id=qr_id)

    if not qr.imagen_qr:
        return HttpResponse("No hay imagen QR generada", status=404)

    file_path = os.path.join(settings.MEDIA_ROOT, qr.imagen_qr.name)

    try:
        f = open(file_path, 'rb')  # ❗️ No usamos "with"
        mime_type, _ = mimetypes.guess_type(file_path)
        return FileResponse(f, content_type=mime_type or 'application/octet-stream', as_attachment=True, filename=f"{qr.nombre}.png")
    except FileNotFoundError:
        return HttpResponse("Archivo no encontrado", status=404)

def descargar_qr_pdf(request, qr_id):
    qr = get_object_or_404(QRCode, id=qr_id)
    if not qr.imagen_qr:
        return HttpResponse("No hay imagen QR generada", status=404)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    c.setFont("Helvetica-Bold", 18)
    c.drawString(100, 800, f"Código QR: {qr.nombre}")

    image_path = os.path.join(settings.MEDIA_ROOT, qr.imagen_qr.name)
    qr_img = ImageReader(image_path)
    c.drawImage(qr_img, 100, 600, width=200, height=200)

    c.setFont("Helvetica", 12)
    c.drawString(100, 570, f"Redirige a: {qr.url_destino}")
    c.drawString(100, 550, f"Visitas: {qr.visitas}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return FileResponse(buffer, content_type='application/pdf', filename=f"{qr.nombre}.pdf")


def detalle_qr(request, qr_id):
    qr = get_object_or_404(QRCode, id=qr_id)
    return render(request, 'detalle_qr.html', {'qr': qr})


def delete_qr_code(request, pk):
    qr = get_object_or_404(QRCode, pk=pk)
    qr.delete()
    messages.success(request, "QR eliminado correctamente.")
    return redirect('listar_qrs')