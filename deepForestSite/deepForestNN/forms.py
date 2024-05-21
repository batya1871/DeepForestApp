from django import forms
from .models import Image_data


class SetImageForm(forms.ModelForm):
    class Meta:
        model = Image_data
        fields = ['source_file']
        widgets = {
            'source_file': forms.ClearableFileInput(attrs={
                'class': 'image-selection',
                'accept': 'image/*'
            })
        }
        labels = {
            'source_file': 'нажмите на эту кнопку, чтобы выбрать изображение'
        }

    def clean_source_file(self):
        file = self.cleaned_data.get('source_file')
        if file:
            if not file.content_type.startswith('image/'):
                raise forms.ValidationError('Загруженный файл не является изображением.')
            if file.size > 5 * 1024 * 1024:  # Ограничение размера файла до 5MB
                raise forms.ValidationError('Размер файла не должен превышать 5MB.')
        return file
