from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import re

class CloudCubeStorage(S3Boto3Storage):
    """
    CloudCube için özel storage sınıfı
    """
    def __init__(self, folder='gonullu_durum_fotolar', *args, **kwargs):
        # CloudCube URL'den cube adını çıkar
        if hasattr(settings, 'CLOUDCUBE_URL') and settings.CLOUDCUBE_URL:
            match = re.match(r'https:\/\/(.*?)\.s3\.amazonaws\.com\/(.*)', settings.CLOUDCUBE_URL)
            if match:
                self.location = f"{match.group(2)}/public/{folder}"
            else:
                self.location = f'public/{folder}'
        else:
            self.location = f'public/{folder}'
            
        self.file_overwrite = False
        super().__init__(*args, **kwargs)

class GonulluDurumStorage(CloudCubeStorage):
    """
    Gönüllü durum fotoğrafları için storage sınıfı
    """
    def __init__(self, *args, **kwargs):
        super().__init__(folder='gonullu_durum_fotolar', *args, **kwargs)

class GonulluSorunStorage(CloudCubeStorage):
    """
    Gönüllü sorun fotoğrafları için storage sınıfı
    """
    def __init__(self, *args, **kwargs):
        super().__init__(folder='gonullu_sorun_fotolar', *args, **kwargs) 