from django.db import connection
import numpy as np

def getstudentcoursewisePLO(studentID, courseID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum as plonum,100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as plopercent
                FROM app_registration_t r,
                    app_assessment_t a, 
                    app_evaluation_t e,
                    app_co_t co, 
                    app_plo_t p
                WHERE  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and r.student_id = '{}'
                    and co.course_id = '{}'
                GROUP BY  p.ploID

                '''.format(studentID, courseID))
        row = cursor.fetchall()
    return row


def getcoursewiseavgPLO(courseID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum as plonum, avg(100*e.obtainedMarks/a.totalMarks)
                FROM app_registration_t r,
                    app_assessment_t a, 
                    app_evaluation_t e,
                    app_co_t co, 
                    app_plo_t p
                WHERE  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and co.course_id = '{}'
                GROUP BY  p.ploID
                '''.format(courseID))
        row = cursor.fetchall()
    return row

def getcompletedcourses(studentID):
    with connection.cursor() as cursor:
        cursor.execute(
            ''' 
                SELECT distinct s.course_id
                FROM app_registration_t r,
                    app_evaluation_t e,
                    app_section_t s
                WHERE  r.registrationID = e.registration_id 
                and r.section_id = s.sectionID
                and r.student_id = '{}'
            '''.format(studentID))
        row = cursor.fetchall()
    return row

def getcorrespondingstudentid(userID):
    with connection.cursor() as cursor:
        cursor.execute(
            ''' 
                SELECT studentID
                FROM app_student_t s
                WHERE s.user_ptr_id = '{}'
            '''.format(userID))
        row = cursor.fetchall()
    return row


def getstudentprogramwisePLO(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum as plonum,100*(sum(e.obtainedMarks)/sum(a.totalMarks)) as plopercent
                FROM app_registration_t r,
                    app_assessment_t a, 
                    app_evaluation_t e,
                    app_co_t co, 
                    app_plo_t p,
                    app_student_t s,
                    app_program_t pr
                WHERE  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and r.student_id = '{}'
                    and s.studentID = r.student_id
                    and s.program_id = pr.programID
                GROUP BY  p.ploID
                '''.format(studentID))
        row = cursor.fetchall()
    return row


def getprogramwiseavgPLO(programID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT p.ploNum as plonum, avg(100*e.obtainedMarks/a.totalMarks)
                FROM app_registration_t r,
                    app_assessment_t a, 
                    app_evaluation_t e,
                    app_co_t co, 
                    app_plo_t p
                WHERE  r.registrationID = e.registration_id 
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and p.program_id = '{}'
                GROUP BY  p.ploID
                '''.format(programID))
        row = cursor.fetchall()
    return row


def getstudentprogramid(studentID):
    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT s.program_id
                FROM app_student_t s
                WHERE s.studentID = '{}'
                '''.format(studentID))
        row = cursor.fetchall()
    return row


def getstudentallcoursePLO(studentID, category):
    with connection.cursor() as cursor:
        cursor.execute(''' 
               SELECT p.ploNum as ploNum,co.course_id,sum(e.obtainedMarks),sum(a.totalMarks), derived.Total
               FROM app_registration_t r,
                   app_assessment_t a, 
                   app_evaluation_t e,
                   app_co_t co, 
                   app_plo_t p,
                   (
                        SELECT p.ploNum as ploNum,sum(a.totalMarks) as Total, r.student_id as StudentID
                        FROM app_registration_t r,
                            app_assessment_t a, 
                            app_evaluation_t e,
                            app_co_t co, 
                            app_plo_t p
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and r.student_id = '{}'
                        GROUP BY  r.student_id,p.ploID) derived
               WHERE r.student_id = derived.StudentID
                    and e.registration_id = r.registrationID
                    and e.assessment_id = a.assessmentID
                    and a.co_id=co.coID 
                    and co.plo_id = p.ploID
                    and p.ploNum = derived.ploNum

               GROUP BY  p.ploID,co.course_id

               '''.format(studentID))
        row = cursor.fetchall()

    table = []
    courses = []

    for entry in row:
        if entry[1] not in courses:
            courses.append(entry[1])
    courses.sort()
    plo = ["PLO1", "PLO2", "PLO3", "PLO4", "PLO5", "PLO6", "PLO7", "PLO8", "PLO9", "PLO10", "PLO11", "PLO12"]

    for i in courses:
        temptable = []
        if category == 'report':
            temptable = [i]

        for j in plo:
            found = False
            for k in row:
                if j == k[0] and i == k[1]:
                    if category == 'report':
                        temptable.append(np.round(100 * k[2] / k[3], 2))
                    elif category == 'chart':
                        temptable.append(np.round(100 * k[2] / k[4], 2))
                    found = True
            if not found:
                if category == 'report':
                    temptable.append('N/A')
                elif category == 'chart':
                    temptable.append(0)
        table.append(temptable)
    return plo, courses, table


def getfacultycoursewisePLO(courseID, semesters):
    sem = '';
    for semester in semesters:
        sem += '"'
        sem += semester
        sem += '",'

    sem = sem[:-1]

    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT f.first_name, f.last_name, f.plonum, COUNT(*) as achieved_cnt
                FROM
                (
                    SELECT u.first_name, u.last_name, p.ploNum as plonum, 100*e.obtainedMarks/a.totalMarks as percentage
                    FROM app_registration_t r, 
                        app_assessment_t a, 
                        app_evaluation_t e, 
                        app_co_t co, 
                        app_plo_t p, 
                        app_section_t s,
                        accounts_user u,
                        app_employee_t emp
                    WHERE r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID 
                        and a.co_id=co.coID 
                        and co.plo_id = p.ploID 
                        and a.section_id = s.sectionID
                        and s.faculty_id IN 
                        ( 
                            SELECT DISTINCT s.faculty_id 
                            FROM app_section_t s 
                            WHERE s.course_id = '{}'
                        ) 
                        and s.semester IN ({})
                        and s.course_id ='{}'
                        and s.faculty_id = emp.employeeID
                        and emp.user_ptr_id = u.id
                )f
                WHERE f.percentage >= 40
                GROUP BY f.first_name, f.plonum;
               '''.format(courseID, sem, courseID))
        row1 = cursor.fetchall()

        cursor.execute('''
                SELECT COUNT(*)
                FROM
                (
                    SELECT u.first_name, u.last_name, p.ploNum as plonum, 100*e.obtainedMarks/a.totalMarks as percentage
                    FROM app_registration_t r, 
                        app_assessment_t a, 
                        app_evaluation_t e, 
                        app_co_t co, 
                        app_plo_t p, 
                        app_section_t s,
                        accounts_user u,
                        app_employee_t emp
                    WHERE r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID 
                        and a.co_id=co.coID 
                        and co.plo_id = p.ploID 
                        and a.section_id = s.sectionID
                        and s.faculty_id IN 
                        ( 
                            SELECT DISTINCT s.faculty_id 
                            FROM app_section_t s 
                            WHERE s.course_id = '{}'
                        ) 
                        and s.semester IN ({})
                        and s.course_id ='{}'
                        and s.faculty_id = emp.employeeID
                        and emp.user_ptr_id = u.id
                )f
                GROUP BY f.first_name, f.plonum;
               '''.format(courseID, sem, courseID))
        row2 = cursor.fetchall()
        
        faculty = []
        plonum = []
        plos1 = []
        plos2 = []

        for record in row1:
            faculty.append(record[0]+' '+record[1])
            plonum.append(record[2])
            plos1.append(record[3])

        for record in row2:
            plos2.append(record[0])

        plos = 100*(np.array(plos1)/np.array(plos2))
        plos = plos.tolist()

        faculty = list(set(faculty))
        plonum = list(set(plonum))

        plonum.sort()
        plonum.sort(key=len, reverse=False)

        plos = np.array(plos)
        plos = np.split(plos, len(plos)/len(plonum))
        
        new_plo=[]
        for plo in plos:
            new_plo.append(plo.tolist())

        return faculty, plonum, new_plo


def getsemestercoursewisePLO(courseID, semesters):
    sem = '';
    for semester in semesters:
        sem += '"'
        sem += semester
        sem += '",'

    sem = sem[:-1]

    with connection.cursor() as cursor:
        cursor.execute(''' 
                    SELECT f.semester, f.plonum, COUNT(*) as achieved_cnt
                    FROM
                    (
                        SELECT s.semester, p.ploNum as plonum, s.course_id, 100*e.obtainedMarks/a.totalMarks as percentage
                        FROM app_registration_t r, 
                            app_assessment_t a, 
                            app_evaluation_t e, 
                            app_co_t co, 
                            app_plo_t p, 
                            app_section_t s
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID 
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and a.section_id = s.sectionID
                            and s.semester IN ({})
                            and co.course_id ='{}'
                            and s.course_id = co.course_id
                    )f
                    WHERE f.percentage >= 40
                	GROUP BY f.semester, f.plonum;
               '''.format(sem, courseID))
        row1 = cursor.fetchall()

        cursor.execute('''
                SELECT COUNT(*) as all_cnt
                    FROM
                    (
                        SELECT s.semester, p.ploNum as plonum, s.course_id, 100*e.obtainedMarks/a.totalMarks as percentage
                        FROM app_registration_t r, 
                            app_assessment_t a, 
                            app_evaluation_t e, 
                            app_co_t co, 
                            app_plo_t p, 
                            app_section_t s
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID 
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and a.section_id = s.sectionID
                            and s.semester IN ({})
                            and co.course_id ='{}'
                            and s.course_id = co.course_id
                    )f
                	GROUP BY f.semester, f.plonum;
               '''.format(sem, courseID))
        row2 = cursor.fetchall()


        semester = []
        plonum = []
        acheived = []
        all_cnt = []

        for record in row1:
            semester.append(record[0])
            plonum.append(record[1])
            acheived.append(record[2])

        for record in row2:
            all_cnt.append(record[0])

        acheived_per = 100*(np.array(acheived)/np.array(all_cnt))

        semester = list(set(semester))
        plonum = list(set(plonum))

        failed_per = 100 - acheived_per

        acheived_per = np.split(acheived_per, len(acheived_per)/len(semester))
        failed_per = np.split(failed_per, len(failed_per)/len(semester))
        
        acheived=[]
        for plo in acheived_per:
            acheived.append(plo.tolist())

        failed=[]
        for plo in failed_per:
            failed.append(plo.tolist())

        return semester, plonum, acheived, failed

                            
def getplowisecoursecomparism(plos, semesters):
    sem = '';
    for semester in semesters:
        sem += '"'
        sem += semester
        sem += '",'

    sem = sem[:-1]

    ploo = '';
    for plo in plos:
        ploo += '"'
        ploo += plo
        ploo += '",'

    ploo = ploo[:-1]

    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT f.course_id, f.ploNum, COUNT(*) 
                FROM 
                    ( 
                        SELECT s.course_id, p.ploNum, 100*e.obtainedMarks/a.totalMarks as percentage 
                        FROM app_registration_t r, 
                            app_assessment_t a, 
                            app_evaluation_t e, 
                            app_co_t co, 
                            app_plo_t p, 
                            app_section_t s 
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID 
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and p.ploNum in ({}) 
                            and a.section_id = s.sectionID 
                            and s.semester IN ({}) 
                    )f 
                WHERE f.percentage >= 40 
                GROUP BY f.ploNum, f.course_id;
               '''.format(ploo, sem))
        row1 = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT COUNT(*) 
                FROM 
                    ( 
                        SELECT s.course_id, p.ploNum, 100*e.obtainedMarks/a.totalMarks as percentage 
                        FROM app_registration_t r, 
                            app_assessment_t a, 
                            app_evaluation_t e, 
                            app_co_t co, 
                            app_plo_t p, 
                            app_section_t s 
                        WHERE r.registrationID = e.registration_id 
                            and e.assessment_id = a.assessmentID 
                            and a.co_id=co.coID 
                            and co.plo_id = p.ploID 
                            and p.ploNum in ({}) 
                            and a.section_id = s.sectionID 
                            and s.semester IN ({}) 
                    )f
                GROUP BY f.ploNum, f.course_id;
               '''.format(ploo, sem))
        row2 = cursor.fetchall()
    
        courses = []
        plonum = []
        acheived = []
        all_cnt = []

        for record in row1:
            courses.append(record[0])
            plonum.append(record[1])
            acheived.append(record[2])

        for record in row2:
            all_cnt.append(record[0])

        acheived_per = 100*(np.array(acheived)/np.array(all_cnt))

        courses = list(set(courses))
        plonum = list(set(plonum))

        acheived_per = np.split(acheived_per, len(acheived_per)/len(plonum))
        
        acheived=[]
        for plo in acheived_per:
            acheived.append(plo.tolist())

        return courses, plonum, acheived


def getprogramsemesterwiseplocount(program, semesters):
    sem = '';
    for semester in semesters:
        sem += '"'
        sem += semester
        sem += '",'
    
    sem = sem[:-1]

    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT f.plonum, COUNT(*)
                FROM
                (
                    SELECT p.ploNum as plonum, r.student_id, 100*e.obtainedMarks/a.totalMarks as percentage
                    FROM app_registration_t r, 
                        app_assessment_t a, 
                        app_evaluation_t e, 
                        app_co_t co, 
                        app_plo_t p, 
                        app_section_t s,
                        app_program_t prog
                    WHERE r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID 
                        and a.co_id=co.coID 
                        and co.plo_id = p.ploID 
                        and p.program_id = prog.programID
                        and prog.programName = '{}'
                        and a.section_id = s.sectionID
                        and s.semester IN ({})
                )f
                WHERE f.percentage>=40
                GROUP BY f.plonum;
               '''.format(program, sem))
        row1 = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT COUNT(*)
                FROM
                (
                    SELECT p.ploNum as plonum, r.student_id, 100*e.obtainedMarks/a.totalMarks as percentage
                    FROM app_registration_t r, 
                        app_assessment_t a, 
                        app_evaluation_t e, 
                        app_co_t co, 
                        app_plo_t p, 
                        app_section_t s,
                        app_program_t prog
                    WHERE r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID 
                        and a.co_id=co.coID 
                        and co.plo_id = p.ploID 
                        and p.program_id = prog.programID
                        and prog.programName = '{}'
                        and a.section_id = s.sectionID
                        and s.semester IN ({})
                )f
                GROUP BY f.plonum;
            '''.format(program, sem))
        row2 = cursor.fetchall()

        plonum = []
        acheived = []
        attempted = []

        for record in row1:
            plonum.append(record[0])
            acheived.append(record[1])

        for record in row2:
            attempted.append(record[0])

        plonum = list(set(plonum))

        acheived = np.array(acheived)
        attempted = np.array(attempted)

        new_acheived=[]
        for plo in acheived:
            new_acheived.append(plo.tolist())

        new_attempted=[]
        for plo in attempted:
            new_attempted.append(plo.tolist())

        plonum.sort()
        plonum.sort(key=len, reverse=False)

        return plonum, new_acheived, new_attempted


def getprogramwiseploandcourses(program, semesters):
    sem = '';
    for semester in semesters:
        sem += '"'
        sem += semester
        sem += '",'
    
    sem = sem[:-1]

    with connection.cursor() as cursor:
        cursor.execute(''' 
                SELECT f.ploNum, f.course_id, COUNT(*)
                FROM
                (
                    SELECT p.ploNum as plonum, s.course_id, r.student_id, 100*e.obtainedMarks/a.totalMarks as percentage
                    FROM app_registration_t r, 
                        app_assessment_t a, 
                        app_evaluation_t e, 
                        app_co_t co, 
                        app_plo_t p, 
                        app_section_t s,
                        app_program_t prog
                    WHERE r.registrationID = e.registration_id 
                        and e.assessment_id = a.assessmentID 
                        and a.co_id=co.coID 
                        and co.plo_id = p.ploID 
                        and p.program_id = prog.programID
                        and prog.programName = '{}'
                        and a.section_id = s.sectionID
                        and s.semester IN ({})
                    )f
                    WHERE f.percentage>=40
                    GROUP BY f.ploNum, f.course_id
               '''.format(program, sem))
        row = cursor.fetchall()

        plonum = []
        courses = []
        counts = []

        for record in row:
            plonum.append(record[0])
            courses.append(record[1])

        plonum = list(set(plonum))
        plonum.sort()
        plonum.sort(key=len, reverse=False)

        courses = list(set(courses))
        courses.sort()


        table = np.zeros((len(courses), len(plonum)))


        for record in row:
            table[courses.index(record[1])][plonum.index(record[0])] += record[2]

        table = table.tolist()

        return plonum, courses, table