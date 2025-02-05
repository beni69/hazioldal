from django.contrib import admin
from .models import Git,Tanit, Mentoral, Temakor, Feladat, Tartozik, Kituzes, Hf, Mo, Biralat, Egyes, Haladek_kerelem, HaziCsoport

##############################
### GIT

def mentoraltszam_frissitese(modeladmin, request, queryset):
    for hazioldal_user in queryset:
        hazioldal_user.update_counts_mentoralt_miatt()
mentoraltszam_frissitese.short_description = "miből-mennyi frissítése hf alapján mentorált miatt" 
 

def mentorszam_frissitese(modeladmin, request, queryset):
    for hazioldal_user in queryset:
        hazioldal_user.update_counts_mentor_miatt()
mentorszam_frissitese.short_description = "miből-mennyi frissítése hf alapján mentor miatt"


def user_hazijainak_frissitese(modeladmin, request, queryset):
    for hazioldal_user in queryset:
        for hf in Hf.objects.filter(user = hazioldal_user.user):
            hf.update_allapot()
user_hazijainak_frissitese.short_description = "Hf-einek frissítése" 


def hazifeladataik_szinkronizalasa(modeladmin, request, queryset):
    kituzesek = set()
    kituzesei = {}
    for hazioldal_user in queryset:
        kituzesei[hazioldal_user] = set([(hf.kituzes, hf.hatarido) for hf in Hf.objects.filter(user = hazioldal_user.user)])
        kituzesek.update(kituzesei[hazioldal_user]) # update = in-place-union
        
    for hazioldal_user in queryset:
        for a_kituzes, a_hatarido in kituzesek.difference(kituzesei[hazioldal_user]):
            a_hf, created = Hf.objects.get_or_create(kituzes=a_kituzes, user=hazioldal_user.user, hatarido=a_hatarido)
            if created:
                a_hf.update_allapot()
                a_hf.user.git.update_counts_mentoralt_miatt()
hazifeladataik_szinkronizalasa.short_description = "Házi feladataik szinkronizálása" 


class GitAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'email')
    # ordering = ['ev']
    actions = [
            mentoraltszam_frissitese,
            mentorszam_frissitese,
            user_hazijainak_frissitese,
            hazifeladataik_szinkronizalasa,
        ]
    list_per_page = 200

admin.site.register(Git, GitAdmin)


##############################
### HF

def allapot_count_update(modeladmin, request, queryset):
    for hf in queryset:
        hf.update_allapot()
allapot_count_update.short_description = "Állapot frissítése"

class HfAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'email')
    # ordering = ['ev']
    actions = [
            allapot_count_update,
        ]
    list_per_page = 1000

admin.site.register(Hf, HfAdmin)


##############################
### Egyes

def egyesek_kretazottra_allitasa(modeladmin, request, queryset):
    for egyes in queryset:
        egyes.kreta = True
        egyes.save()
egyesek_kretazottra_allitasa.short_description = "legyenek krétázva"

def egyesek_kretazatlanra_allitasa(modeladmin, request, queryset):
    for egyes in queryset:
        egyes.kreta = False
        egyes.save()
egyesek_kretazatlanra_allitasa.short_description = "legyenek krétázatlanok"

class EgyesAdmin(admin.ModelAdmin):
    # list_display = ('first_name', 'last_name', 'email')
    # ordering = ['ev']
    list_filter = ["kreta"]
    actions = [
            egyesek_kretazottra_allitasa,
            egyesek_kretazatlanra_allitasa,
        ]
    list_per_page = 1000

admin.site.register(Egyes, EgyesAdmin)

##############################
### 

##############################
###  AUTO-adminok

admin.site.register(Tanit)
admin.site.register(Mentoral)
admin.site.register(Temakor)
admin.site.register(Feladat)
admin.site.register(Tartozik)
admin.site.register(Kituzes)
admin.site.register(Mo)
admin.site.register(Biralat)
admin.site.register(Haladek_kerelem)
admin.site.register(HaziCsoport)

# a trükkös admin-funkciókról, függvényekről az szlgbp_ma_heroku gitrepoban vannak jó példák.

