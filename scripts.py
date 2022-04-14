import random
from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation, Subject


def find_schoolkid_by_name(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except Schoolkid.DoesNotExist:
        print(f'Не удалось найти ученика с именем {schoolkid_name}')
        return False
    except Schoolkid.MultipleObjectsReturned:
        full_names = [kid.full_name for kid in Schoolkid.objects.filter(full_name__contains=schoolkid_name)]
        print(f'Нашлось больше одного ученика: {full_names}')
        return False


def fix_marks_on_five(schoolkid_name):
    schoolkid = find_schoolkid_by_name(schoolkid_name)
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def fix_marks(schoolkid_name):
    schoolkid = find_schoolkid_by_name(schoolkid_name)
    bad_marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3])
    for bad_mark in bad_marks:
        bad_mark.points = random.choice([4, 5])
        bad_mark.save()


def remove_chastisements(schoolkid_name):
    schoolkid = find_schoolkid_by_name(schoolkid_name)
    bad_opinions = Chastisement.objects.filter(schoolkid=schoolkid)
    bad_opinions.delete()


def create_commendation(schoolkid_name, subject_name):
    schoolkid = find_schoolkid_by_name(schoolkid_name)
    kid_lessons_on_subject = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                                   group_letter=schoolkid.group_letter,
                                                   subject__title=subject_name)

    if not kid_lessons_on_subject:
        print(f'Предмета с названием "{subject_name}" у ученика {schoolkid.full_name} не удалось найти!')
        subjects = Subject.objects.filter(year_of_study=schoolkid.year_of_study)
        subjects_names = ', '.join([subject.title for subject in subjects])
        print(f'Вот полный список предметов для {schoolkid.full_name}:\n{subjects_names}')
        return None

    choice_list = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!']
    text = random.choice(choice_list)
    lesson = random.choice(kid_lessons_on_subject)
    Commendation.objects.create(text=text, created=lesson.date, schoolkid=schoolkid, subject=lesson.subject,
                                teacher=lesson.teacher)

