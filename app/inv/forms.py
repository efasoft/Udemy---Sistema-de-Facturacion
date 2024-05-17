from django import forms

from .models import Categoria, SubCategoria, Marca, \
  UnidadMedida, Producto


class CategoriaForm(forms.ModelForm):
    class Meta:
        model=Categoria
        fields = ['descripcion','estado']
        labels = {'descripcion':"Descripción de la Categoría",
               "estado":"Estado"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            })

class SubCategoriaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.filter(estado=True)
        .order_by('descripcion')
    )
    class Meta:
        model=SubCategoria
        fields = ['categoria','descripcion','estado']
        labels = {'descripcion':"Sub Categoría",
               "estado":"Estado"}
        widget={'descripcion': forms.TextInput}

    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class':'form-control'
            }) 
        self.fields['categoria'].empty_label = "Seleccione Categoria"

class MarcaForm(forms.ModelForm):
    class Meta:
        model=Marca
        fields = ['descripcion','estado']
        labels= {'descripcion': "Descripción de la Marca",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

class UMForm(forms.ModelForm):
    class Meta:
        model=UnidadMedida
        fields = ['descripcion','estado']
        labels= {'descripcion': "Descripción de la Marca",
                "estado":"Estado"}
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })

                   
class ProductoForm(forms.ModelForm):
    class Meta:
        model=Producto
        fields=['codigo','codigo_barra','descripcion','estado', \
                'precio','existencia','ultima_compra',
                'marca','subcategoria','unidad_medida','foto']
        exclude = ['um','fm','uc','fc']
        widget={'descripcion': forms.TextInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
        self.fields['ultima_compra'].widget.attrs['readonly'] = True
        self.fields['existencia'].widget.attrs['readonly'] = True

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')

        if codigo:
            codigo = codigo.upper()
            self.cleaned_data['codigo'] = codigo  # Actualiza cleaned_data con el código en mayúsculas
            try:
                producto_existente = Producto.objects.get(codigo=codigo)
                if not self.instance.pk:
                    raise forms.ValidationError("Registro ya existe")
                elif self.instance.pk != producto_existente.pk:
                    raise forms.ValidationError("Cambio no permitido, coincide con otro registro")
            except Producto.DoesNotExist:
                pass

        return codigo

    def clean(self):
        cleaned_data = super().clean()
        # Aquí puedes agregar cualquier limpieza adicional si es necesario
        return cleaned_data

#    def clean(self):
#        try:
#            sc = Producto.objects.get(
#                codigo = self.cleaned_data['codigo'].upper()
#            )
#            if not self.instance.pk:
#                raise forms.ValidationError("Registro ya existe")
#            elif self.instance.pk!= sc.pk:
#                raise forms.ValidationError("Cambio no permitido, coincide con otro registro")
#        except Producto.DoesNotExist:
#            pass
#        return self.changed_data
#
#   Codigo mejorado por ChaGPT
"""
    def clean(self):
        cleaned_data = super().clean()
        codigo = cleaned_data.get('codigo')
       
        if codigo:
            codigo = codigo.upper()
            try:
                producto_existente = Producto.objects.get(codigo=codigo)
                if not self.instance.pk:
                    raise forms.ValidationError("Registro ya existe")
                elif self.instance.pk != producto_existente.pk:
                    raise forms.ValidationError("Cambio no permitido, coincide con otro registro")
            except Producto.DoesNotExist:
                pass

        return self.changed_data
"""
# Codigo mejorado por ChaGPT


    
#