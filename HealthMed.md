# Структура проекта

Сайт написан при помощи веб-фреймворка [django-rest-framework](https://www.django-rest-framework.org/).

## Как запустить проект
1. Установить на компьютер [docker](https://docker.com)
2. Распаковать архив `HealthMedProject.rar`
3. Открыть терминал в корневой папке проекта и написать в консоле docker `docker compose build`, а затем `docker compose up`
4. Запуститься 3 контейнера: nginx, postgresql и python с кодом самого сайта

---

## Приложения

Проект состоит из 3 приложений (не считая основного healthmed): 
1. main_pages
2. users
3. doctors

---

### main_pages
Данное приложение отвечает за главную страницу и страницу со статьями.
Также основные scss стили из данного приложения подключаются во всех остальных.

Редиректы приложения:
```python
path('', views.MainIndexAPIView.as_view(), name="main"),
path('articles/', views.ArticlesAPIView.as_view(), name="articles"),
```

Дерево файлов приложения:
```python
MAIN_PAGES
│   admin.py
│   apps.py
│   defs.py
│   models.py
│   tests.py
│   urls.py
│   views.py
│   __init__.py
│
├───static
│   └───main_pages
│       ├───forms
│       │       login_in.html
│       │       registration.html
│       │       success.html
│       │
│       ├───images
│       │       block-1.png
│       │       hospital-image.png
│       │       hospital-image.pnghospital-image.png
│       │       med-art.jpg
│       │       med-art.png
│       │       notepad-image.png
│       │       notepad-image.pngnotepad-image.png
│       │
│       ├───js
│       │       actions.js
│       │       handlers.js
│       │       login-form.js
│       │       register-form.js
│       │
│       └───styles
│               footer.css
│               footer.css.map
│               footer.scss
│               forms.css
│               forms.css.map
│               forms.scss
│               header.css
│               header.css.map
│               header.scss
│               index.css
│               index.css.map
│               index.scss
│               monitor.sh
│
└───templates
    └───main_pages
            articles.html
            index.html
```
---

### users
Данное приложение отвечает за личный кабинет пользователя, а также за обработку запросов api, связанных с действиями пользователя.
Редиректы данного приложения:

*(в начале пути стоит user/, а затем то, что в path первым аргументом)*
```python
path('profile/', views.UsersIndexAPIView.as_view(), name="profile"),
path('api/registerPatient', views.RegisterPatient.as_view()),
path('api/loginPatient', views.LoginPatient.as_view()),
path('api/logOut', views.LogOut.as_view()),
path('api/renderWorkspace', views.RenderProfileWorkspace.as_view()),
path('api/makeAppointment', views.MakePatientAppointment.as_view()),
path('api/denyAppointment', views.DenyPatientAppointment.as_view()),
path('api/editInfo', views.EditPatientData.as_view()),
path('api/makeConsultationRequest', views.MakePatientConsultationRequest.as_view()),
path('api/deleteConsultation', views.DeletePatientConsultationRequest.as_view()),
```

Дерево файлов приложения:
```python
USERS
│   admin.py
│   apps.py
│   backends.py
│   classes.py
│   defs.py
│   models.py
│   serializers.py
│   tests.py
│   urls.py
│   utils.py
│   validators.py
│   views.py
│   __init__.py
│
├───static
│   └───users
│       ├───js
│       │       patient-consultations.js
│       │       patient-profile.js
│       │       patient-schedule.js
│       │
│       └───styles
│               personal_cabinet.css
│               personal_cabinet.css.map
│               personal_cabinet.scss
│
└───templates
    └───users
        │   user_cabinet.html
        │
        └───workspaces
                user_appointment.html
                user_consultation.html
                user_history.html
                user_tables.html
```
---

### doctors
Данное приложение отвечает за личный кабинет врача и вход в него. Также обрабатывает запросы на роуты api, связанные с врачами.
Эндпоинты, за которые отвечает приложение:

*(в начале пути стоит doctor/, а затем то, что в path первым аргументом)*
```python
path('api/getBySpecializationId', views.GetDoctorsBySpecializationId.as_view()),
path('api/getSchedule', views.GetDoctorSchedule.as_view()),
path('api/renderWorkspace', views.RenderProfileWorkspace.as_view()),
path('api/addScheduleRecord', views.AddDoctorScheduleRecord.as_view()),
path('api/deleteScheduleRecord', views.DeleteDoctorScheduleRecord.as_view()),
path('api/acceptConsultation', views.AcceptConsultation.as_view()),
path('api/denyConsultation', views.DenyConsultation.as_view()),
path('api/createArticle', views.CreateArticle.as_view()),
path('api/deleteArticle', views.DeleteArticle.as_view()),
path('profile', views.DoctorIndexAPIView.as_view(), name="doctor-profile"),
path('', views.DoctorIndexAPIView.as_view()),
path('login', views.DoctorLoginAPIView.as_view(), name="doctor-login"),
```

Дерево файлов приложения:
```python
DOCTORS
│   admin.py
│   apps.py
│   backends.py
│   models.py
│   serializers.py
│   tests.py
│   urls.py
│   views.py
│   __init__.py
│
├───static
│   └───doctors
│       ├───js
│       │       doctor-article.js
│       │       doctor-consultations.js
│       │       doctor-profile.js
│       │       doctor-schedule.js
│       │
│       └───styles
│               doctor_cabinet.css
│               doctor_cabinet.css.map
│               doctor_cabinet.scss
│               login.css
│               login.css.map
│               login.scss
│
└───templates
    └───doctors
        │   doctor_cabinet.html
        │   login.html
        │   register.html
        │
        └───workspaces
                doctor_appointments.html
                doctor_article.html
                doctor_consultation.html
                doctor_schedule.html
```

# Модели приложений

Модель - по факту описание таблицы в базе данных PostgreSQL (в моём случае), в которой заранее чётко прописаны типы полей и поведение модели.
У приложений users и doctors есть свои модели, описанные в файле `models.py`

Поверх моделей существуют также сериализаторы. Они отвечают за валидацию данных, которые поступили от пользователя.
Т.е. благодаря им, автоматизируется проверка данных и, если возникает несоответсвие с типом данных, то возвращается ошибка с указанием на поле.
Все сериализаторы описаны в файлах `serializers.py` в приложениях doctos и users (названия сериализатором соответсвует названиям моделей, но с припиской `Serializer` в конце)

## Модели приложения users

```python
class Patient(AbstractBaseUser):
    patient_id = models.AutoField(primary_key=True)

    email = models.EmailField(null=False, unique=True)
    phone = PhoneNumberField(null=False, unique=True)
    password = models.CharField(max_length=256, null=False)

    firstname = models.CharField(max_length=32, null=False)
    lastname = models.CharField(max_length=32, null=False)
    surname = models.CharField(max_length=32, null=True, default=None)

    birthdate = models.DateField()
    passport = models.CharField(max_length=10, null=False, unique=True)
    med_policy = models.CharField(max_length=16, null=False, unique=True)

    last_login = models.DateTimeField(null=True) # Служебное поле, требующееся для работы сессий (захода в аккаунт)
    is_active = models.BooleanField(default=True) # Служебое поле, требующееся для работы сессий (захода в аккаунт)


    def get_username(self): # Функция, возвращающая поле, по которому человек логинится (email)

    def get_phone(self): # Функция, возвращающая номер телефона пользователя
    
    def get_self_record(self): # Функция, возвращающая запись самого пользователя по его id

    def appointment_schedule(cls, patient_id: int, doctor_id: int, schedule_id: int): # Функция, записывающая человека на приём к врачу по заданным параметрам
    
    def custom_update(self, *args, **kwargs): # Функция, обрабатывающая данные, поступившие для обновления личных данных пользователя

    def to_dict(self): # Возвращает запись в виде json формата
  
  

class Consultation(models.Model):
    consultation_id = models.AutoField(primary_key=True)
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    date = models.DateField()
    status = models.BooleanField(null=True, default=None) # Статус заявки на конультацию (null = ожидает подтверждения, True/False = принято/отказано соответсвенно)  

    def to_dict(self): # Возвращает запись в виде json формата
  
  

class Appointment(models.Model):
    appointment_id = models.AutoField(primary_key=True)

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    schedule = models.ForeignKey(DoctorSchedule, on_delete=models.CASCADE) # Ссылка на запись расписания врача
    
    def to_dict(self): # Возвращает запись в виде json формата
```

## Модели приложения doctors


```python
class DoctorSpecialization(models.Model):

    """

        Модель для объекта DoctorSpecialization для хранения специализаций врачей
        
        specialization_id - первичный ключ модели создается автоматически и принимает значение типом данных AutoField.
        specialization_name - строковое поле с максимальной длиной 128 символов, которое обязательно для заполнения. В админ панели оно будет отображаться как "Название".

    """

    specialization_id = models.AutoField(primary_key=True)

    specialization_name = models.CharField("Название", max_length=128, null=False)
    
    def to_dict(self): # Возвращает запись в виде json формата
  
  

class Doctor(AbstractBaseUser):

    """

        Модель для объекта Doctor для хранения данных о врачах

  

        doctor_id - это первичный ключ модели, который автоматически увеличивается с каждым новым экземпляром.
        email - поле для адреса электронной почты, с максимальной длиной 64 символа и уникальным для каждого экземпляра (unique=True).
        password - поле для хранения пароля доктора.
        firstname, lastname, и surname - поля, чтобы хранить имя, фамилия, и отчество доктора соответственно.
        specialization - поле, которое связывает доктора с их специализацией, используя внешний ключ.
        last_login - поле, которое хранит дату и время последнего входа доктора.
        is_active - булево поле, указывающее, активен ли пользователь.

    """

    doctor_id = models.AutoField(primary_key=True)
    
    email = models.CharField("Email", max_length=64, null=False, unique=True)
    password = models.CharField("Пароль", max_length=256, null=False)

    firstname = models.CharField("Имя", max_length=32, null=False)
    lastname = models.CharField("Фамилия", max_length=32, null=False)
    surname = models.CharField("Отчество", max_length=32, null=True, default=None)

    specialization = models.ForeignKey(DoctorSpecialization, on_delete=models.DO_NOTHING, verbose_name="Специализация")
    
    last_login = models.DateTimeField(null=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    def get_username(self): # Возвращает поле, по которому врач логинится (email)
    
    def to_dict(self, with_schedule: bool = False, protected: bool = False): # Возвращает запись в виде json формата

    @classmethod
    def check_exists_by_id(cls, doctor_id: int): # Функция, проверяющая существование врача по его id

    def get_schedule(self): # Функция, возвращающая расписание врача в виде json формата, а также удаляет устаревшие записи


class DoctorSchedule(models.Model):

    """

        Модель DoctorSchedule для хранения расписания работы врачей
        
        schedule_id - уникальный идентификатор расписания (тип данных AutoField).
        doctor - поле, связывающее запись расписания с записью врача (тип данных ForeignKey).
        schedule_date - дата работы врача (тип данных DateField).
        schedule_start_time - время начала работы врача (тип данных TimeField).
        schedule_end_time - время окончания работы врача (тип данных TimeField).
        schedule_state - состояние расписания, определяющее свободен ли врач в данный момент (тип данных BooleanField, по умолчанию False, то есть расписание свободно).

    """

    schedule_id = models.AutoField(primary_key=True)

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    schedule_date = models.DateField(null=False)
    schedule_start_time = models.TimeField(null=False)
    schedule_end_time = models.TimeField(null=False)
    
    schedule_state = models.BooleanField(default=False)


class Article(models.Model):

    """

        Модель Article для хранения статей врачей

        article_id - поле типа AutoField и устанавливается как первичный ключ модели, что означает, что оно должно быть уникальным для каждой записи в таблице с данными модели.
        title - поле типа CharField с максимальной длиной символов равной 255, используется для хранения заголовка статьи.
        text - поле типа TextField и используется для хранения текста статьи.
        publisher - поле типа ForeignKey и связывает модель Article с моделью Doctor. Указывается связь многие-к-одному, что означает, что один доктор может быть автором нескольких статей. При удалении записи в модели Doctor, связанные записи в модели Article не будут удалены (установлен параметр on_delete=models.DO_NOTHING).
        publish_date - поле типа DateField и используется для хранения даты публикации статьи.

    """
    article_id = models.AutoField(primary_key=True)
    
    title = models.CharField(max_length=255)
    text = models.TextField()
    
    publisher = models.ForeignKey(Doctor, on_delete=models.DO_NOTHING)
    publish_date = models.DateField()
    
```

# Описание роутов (url путей) приложений

В файле `urls.py` каждого приложения указывается класс, обрабатывающий запрос на определённый путь сайта.
Классы, возвращающие страницу (`html` код) используют рендер, для генерации конкретных `html` файлов из каталога `templates` этого приложения. 

## Роуты приложения main_pages

```python
class MainIndexAPIView(APIView): # Обрабатывает get запрос и рендерит главную страницу (index.html)

class ArticlesAPIView(APIView): # Обрабатывает get запрос и рендерит страницу со статьями (articles.html)
```

## Роуты приложения doctors

```python
class DoctorIndexAPIView(RetrieveAPIView): # Обрабатывает get запрос и рендерит личный кабинет врача (doctor_cabinet.html)

class DoctorLoginAPIView(APIView): # При обработке get запроса возвращает страницу с логинов в аккаунт врача
									# Post запрос обрабатывает данные, введённые в форму логина


class GetDoctorsBySpecializationId(CreateAPIView):  # Обрабатывает get запрос: возвращает список врачей указанной специализации


class AddDoctorScheduleRecord(CreateAPIView): # Обрабатывает post запрос: создаёт запись расписания врача

class DeleteDoctorScheduleRecord(CreateAPIView): # Обрабатывает post запрос: удаляет запись расписания врача


class AcceptConsultation(CreateAPIView): # Обрабатывает post запрос: одобряет заявку на консультацию к врачу

class DenyConsultation(CreateAPIView): # Обрабатывает post запрос: отклоняет заявку на консультацию к врачу


class GetDoctorSchedule(CreateAPIView): # Обрабатывает post запрос: возвращает расписание врача


class RenderProfileWorkspace(RetrieveAPIView): # Обрабатывает get запрос и, в зависимости от аргумента workspace, рендерит вкладку для личного кабинета врача. 
Если аргумент worspace=doctor-appointments -> рендерится doctor_appointments.html
Если аргумент worspace=doctor-schedule -> рендерится doctor_schedule.html
Если аргумент worspace=doctor-consultation -> рендерится doctor_consultation.html
Если аргумент worspace=doctor-article -> рендерится doctor_article.html


class CreateArticle(CreateAPIView):  # Обрабатывает post запрос: создаёт запись статьи в базе

class DeleteArticle(CreateAPIView): # Обрабатывает post запрос: удаляет запись статьи из базы
```


## Роуты приложения users

```python
class UsersIndexAPIView(RetrieveAPIView): # Обрабатывает get запрос и рендерит личный кабинет пациента (user_cabinet.html)

class RegisterPatient(CreateAPIView): # Обрабатывает post запрос: регистрирует пациента в системе

class LoginPatient(CreateAPIView): # Обрабатывает post запрос: отвечает за проверку введённых данных и авторизацию пользователя

class LogOut(CreateAPIView):  # Обрабатывает post запрос: закрывает текущую сессию пользователя сайта

class EditPatientData(CreateAPIView): # Обрабатывает post запрос: изменяет данные о пользователе



class MakePatientAppointment(CreateAPIView): # Обрабатывает post запрос: записывает пациента на приём к врачу

class DenyPatientAppointment(CreateAPIView): # Обрабатывает post запрос: удаляет запись пациента на приём к врачу


class MakePatientConsultationRequest(CreateAPIView): # Обрабатывает post запрос: создаёт запрос на консультацию к врачу

class DeletePatientConsultationRequest(CreateAPIView): # Обрабатывает post запрос: удаляет запрос на консультацию к врачу


class RenderProfileWorkspace(RetrieveAPIView): # Обрабатывает get запрос и, в зависимости от аргумента workspace, рендерит вкладку для личного кабинета пациента. 
Если аргумент worspace=appointment или consultation -> рендерится user_{appointment или consultation}.html
Если аргумент worspace=user-appointments -> рендерится user_tables.html
Если аргумент worspace=history -> рендерится user_history.html
```
