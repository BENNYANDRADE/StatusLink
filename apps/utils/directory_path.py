#TEACHERS
def file_path(instance, filename):
	return 'files/{1}'.format(instance, filename)


def teacher_homework_directory_path(instance, filename):
		# file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
	return 'user_{0}/homeworks/{1}'.format(instance.id_planification.id_list_subject_grade.id_school_staff.id_user.id, filename)


def teacher_resources_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
	return 'user_{0}/resources/{1}'.format(instance.id_planification.id_list_subject_grade.id_school_staff.id_user.id, filename)


#USER'S GENERAL
def user_profile_pic_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
	return 'user_{0}/profile_pictures/{1}'.format(instance.id_user.id, filename)

#USER'S GENERAL
def user_profile_pic_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
	return 'user_{0}/profile_pictures/{1}'.format(instance.id_user.id, filename)


#STUDENTS
# student_profile_pic_directory_path
# def student_profile_pic_directory_path(instance, filename):
# 	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
# 	return 'user_{0}/profile_pictures/{1}'.format(instance.id_user.id, filename)


def student_homeworks_directory_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
	return 'student_user_{0}/homeworks/{1}'.format(instance.id_student.id_user.id, filename)


def student_test_directory_path(instance, filename):
	#Uploads a a file on > users's/tests/file
	return 'student_user_{0}/tests/{1}'.format(instance.id_student.id_user.id, filename)


#GRADES
def grade_class_schedule_path(instance, filename):
	# file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
	return 'grade/{0}/schedule/{1}'.format(instance.grade_name.replace(" ",""), filename)



def subject_path(instance, filename):
	return 'school/{0}/subjects_images/{1}'.format(instance.id_education_level.id_school.school_name, filename)
	

#DASHBOARD
def welcome_message_attachment_path(instance, filename):
	return 'school/{0}/dashboard_attachment/{1}'.format(instance.id_school.school_name, filename)

#INVOICES
def invoices_path(instance, filename):
	return 'school_{0}/student_{1}/{2}'.format(instance.id_school.school_name, instance.student.id_user, filename)


def school_logo_path(instance, filename):
	return 'school/{0}/logos/{1}'.format(instance.school_name.replace(" ",""), filename)
