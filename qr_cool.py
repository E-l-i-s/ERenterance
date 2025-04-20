import qrcode

def show_qr():
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    qr = qrcode.QRCode(border=1)
    qr.add_data(url)
    qr.make(fit=True)
    qr.print_ascii(invert=True)
    print("\nScan this QR code with your phone for the surprise!")

if __name__ == "__main__":
    show_qr()
