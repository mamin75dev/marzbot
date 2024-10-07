import qrcode
from qrcode.image.pure import PyPNGImage

class QrCodeHelper:
    @classmethod
    async def generate_qr_from_subscription(cls, subscription, filename):
        try:
            # qr = qrcode.QRCode(version=4, box_size=100, error_correction=qrcode.constants.ERROR_CORRECT_L)
            # qr.add_data(subscription)
            # qr.make(fit=False)
            # img = qr.make_image(fill_color="black", back_color="white")
            img = qrcode.make(subscription)
            print(type(img))
            await img.save(f'subscriptions/{filename}.png')
            # return img
        except Exception as e:
            print(e)
