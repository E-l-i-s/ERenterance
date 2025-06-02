import qrcode

def show_qr():
    """
    Generates and prints an ASCII QR code that links to a YouTube video.
    """
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    # Create a QRCode object with a small border
    qr = qrcode.QRCode(border=1)
    # Add the URL data to the QRCode
    qr.add_data(url)
    # Generate the QR code, adjusting size to fit the data
    qr.make(fit=True)
    # Print the QR code as ASCII characters in the terminal
    qr.print_ascii(invert=True)
    print("\nScan this QR code with your phone for the surprise!")

if __name__ == "__main__":
    show_qr()
