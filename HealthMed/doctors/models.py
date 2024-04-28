from django.db import models
from django.db.models import Q
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from datetime import datetime
from users.defs import create_password_hash


class DoctorSpecialization(models.Model):
    """
    
        Модель для объекта DoctorSpecialization для хранения специализаций врачей
    
        specialization_id - первичный ключ модели создается автоматически и принимает значение типом данных AutoField. 
        specialization_name - строковое поле с максимальной длиной 128 символов, которое обязательно для заполнения. В админ панели оно будет отображаться как "Название".
    
    """
    
    specialization_id = models.AutoField(primary_key=True)
    specialization_name = models.CharField("Название", max_length=128, null=False)

    class Meta:
        db_table = "doctors_specializations"
        verbose_name = "Специализация"
        verbose_name_plural = "Специализации"
        
    def __str__(self):
        return self.specialization_name

    def to_dict(self):
        return {
            "name": self.specialization_name,
            "id": self.specialization_id
        }


class DoctorManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        dcotor = self.model(
            email=self.normalize_email(email),
        )

        dcotor.set_password(password)
        dcotor.save(using=self._db)
        return dcotor


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

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    REQUIRED_FIELDS = [
        "email",
        "password",
        "firstname",
        "lastname",
        "specialization"
    ]

    class Meta:
        db_table = "doctors"
        verbose_name = "Врач"
        verbose_name_plural = "Врачи"
        
    def __str__(self):
        return f"{self.lastname} {self.firstname} {self.surname}"
    
    def get_username(self):
        return self.email
    
    def get_self_record(self):
        return Doctor.objects.filter(Q(doctor_id=self.doctor_id)).get()
    
    def set_password(self, password):
        self.password = create_password_hash(password=password)
    
    def to_dict(self, with_schedule: bool = False, protected: bool = False):
        result = {
            "doctor_id": self.doctor_id,
            "email": self.email,
            "password": self.password,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "surname": self.surname,
            "specialization": {
                    "id": self.specialization.specialization_id,
                    "name": self.specialization.specialization_name
                },
        }
        if with_schedule:
            result.update({"schedule": self.get_schedule()})
        if protected or with_schedule:
            result.pop("password", "")
            result.pop("email", "")
        
        return result
    
    @classmethod
    def check_exists_by_id(cls, doctor_id: int):
        try:
            doctor = Doctor.objects.get(doctor_id=doctor_id)
            return True
        except Doctor.DoesNotExist:
            return False
    
        
    def get_schedule(self):
        doctor_schedule = DoctorSchedule.objects.filter(Q(doctor_id=self.doctor_id))
        schedule_list = {}
        schedule_list["count_free_days"] = 0
        current_date = datetime.date(datetime.now())
        for schedule in doctor_schedule:
            if schedule.schedule_date < current_date:
                schedule.delete()
                continue
                
            day = schedule.schedule_date.strftime("%d.%m.%Y")
            schedule_list[day] = schedule_list.get(day, []) + [
                {
                    "start_time": schedule.schedule_start_time.strftime("%H:%M:%S"),
                    "end_time": schedule.schedule_end_time.strftime("%H:%M:%S"),
                    "state": schedule.schedule_state,
                    "schedule_id": schedule.schedule_id
                }
            ]
            schedule_list[day] = sorted(schedule_list[day], key=lambda x: x.get("start_time"))
            
            if schedule.schedule_state is False:
                schedule_list["count_free_days"] += 1
        return schedule_list


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

    class Meta:
        db_table = "doctors_schedules"
        verbose_name = "Расписание врача"
        verbose_name_plural = "Расписание врачей"
        
    def __str__(self):
        return f"{self.doctor} | {self.schedule_date} {self.schedule_start_time}-{self.schedule_end_time}"
    
    def to_dict(self):
        return dict(
                id=self.schedule_id,
                date=self.schedule_date,
                start_time=self.schedule_start_time,
                end_time=self.schedule_end_time,
                state=self.schedule_state
        )


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
    
    
    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"

    def __str__(self):
        return self.title
    
    def to_dict(self):
        return dict(
            id=self.article_id,
            title=self.title,
            text=[x.strip() for x in self.text.split("\n") if x.strip()],
            publisher=self.publisher,
            date=self.publish_date
        )
