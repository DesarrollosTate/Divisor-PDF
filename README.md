# Divisor PDF (Andreani)

Al subir de manera masiva pedidos de Andreani, los mismos se generan 4 por hoja.
Esta app lo que hace es dividor 1 por hoja, permitiendo de manera más sencilla su impresión por ZPL


## Dependencias

Para el correcto uso de la app, será necesario instalar en la PC donde querramos usar:

- Python

Paralelamente, en el símbolo de sistema (CMD), en lo posible dentro de la carpeta donde está el archivo split_pdf_labels.py, deberemos instalar:

```
pip install -r requirements.txt

```

Poppler no es necesario, dado que se dejar en la raíz del proyecto, pero el link es este: https://github.com/oschwartz10612/poppler-windows/releases/


## Pasos importantes

1- Es necesario, al archivo .bat, actualizarle la dirección donde nosotros tendremos la raíz del proyecto. Sino el mismo no ejecutará el programa cuando lo llamemos

2- Al igual que el paso anterior, tenemos que colocar la direccion de Poppler correctamente (necesitamos ubicar su Library\bin)

3- Los archivos que leerá el documento se deben llamar "andreani_labels.pdf". Hay que cambiarlo por uno más simple si así lo deseamos
