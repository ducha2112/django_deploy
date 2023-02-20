from django.db import models
from django.contrib.auth.models import User
from PIL import Image



class Profile(models.Model):
    user = models.OneToOneField(User,verbose_name ='Пользователь', on_delete=models.CASCADE)
    img = models.ImageField('Фото пользователя', default ='default.png', upload_to='user_images')

    CHOISES = (('male', 'Мужской пол'), ('femail', 'Женский пол'))
    gender = models.CharField('Пол', max_length=50,choices=CHOISES,default='mail')
    approv = models.BooleanField('Соглашение про отправку уведомлений на почту', default=False)


    def __str__(self):
        return f'Профайл пользователя {self.user.username}'

    def save(self, *args, **kwargs):
        super().save()

        image = Image.open(self.img.path)

        if image.height > 256 or image.width > 256:
            resize = (256,256)
            image.thumbnail(resize)
            image.save(self.img.path)


    class Meta:
        verbose_name = 'Профайл'
        verbose_name_plural = 'Профайлы'
