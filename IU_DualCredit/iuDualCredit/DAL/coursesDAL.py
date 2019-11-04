from DAL import dataAdapter

def termList():

    try:
        sqlTermList = "SELECT Distinct acadterm.ACAD_TERM_CD, acadterm.acad_term \
                        From iuie_academic_terms acadterm \
                        Order By 1" 
        data = dataAdapter.execute(sqlTermList)
        termList = dataAdapter.ConvertToList(data, 1)    
        return termList
    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)



def campusOfInstructionList():
    try:
        
        sqlCampusList = "SELECT Distinct classes.COI_INST_CD FROM  iuie_classes classes Order By 1 " 
        data = dataAdapter.execute(sqlCampusList)
        CampusList = dataAdapter.ConvertToList(data, 0)    
        return CampusList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)

    


def campusOfEnrollmentList():
    try:

        sqlCampusList = "SELECT Distinct classes.COE_INST_CD FROM  iuie_classes classes Order By 1 " 
        data = dataAdapter.execute(sqlCampusList)
        CampusList = dataAdapter.ConvertToList(data, 0)    
        return CampusList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


    


def coursesList(coursenumber, courseName, campusOfInstruction, acadTerm):
    try:

        sqlCoursesQuery = "SELECT classdata.CLS_KEY, classdata.CRS_ID, enrollments.CRS_DESC, acadterm.acad_term, classdata.COI_INST_CD,  \
        classdata.CLS_INSTR_NM, classdata.ENROLLMENT_CAP, classdata.ENROLLMENT_TOTAL,  \
        classdata.ENROLLMENT_CAP - classdata.ENROLLMENT_TOTAL Calculated_Remaining \
        FROM iuie_classes classdata \
        Left Join iuie_academic_terms acadterm \
        on classdata.ACAD_TERM_CD = acadterm.acad_term_cd \
        Left join iuie_enrollments enrollments \
        on classdata.CRS_ID = enrollments.CRS_ID Where 1 = 1 "
    
        if coursenumber:
            sqlCoursesQuery = sqlCoursesQuery + " AND classdata.CRS_ID Like '%" + coursenumber + "%'"

        if courseName:
            sqlCoursesQuery = sqlCoursesQuery + " AND Lower(enrollments.CRS_DESC) Like Lower('%" + courseName + "%')"

        if campusOfInstruction:
            sqlCoursesQuery = sqlCoursesQuery + " AND Lower(classdata.COI_INST_CD) = Lower('" + campusOfInstruction + "')"

        if acadTerm:
            sqlCoursesQuery = sqlCoursesQuery + " AND classdata.ACAD_TERM_CD = '" + acadTerm + "'"

        sqlCoursesQuery = sqlCoursesQuery + " Order by 2 "

        #print(sqlCoursesQuery)

        data = dataAdapter.execute(sqlCoursesQuery)

        #print(data)

        return data

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


    



def courseDetailView(courseID,term,CampusOfInstruction):

    try:

        sqlCourseDetailViewHeader1 = "SELECT  classdata.CRS_ID, enrollments.CRS_DESC,  \
                acadterm.acad_term, classdata.COE_INST_CD, classdata.COI_INST_CD \
                from iuie_classes classdata  \
                Left Join iuie_academic_terms acadterm \
                on classdata.ACAD_TERM_CD = acadterm.acad_term_cd \
                Left join iuie_enrollments enrollments \
                on classdata.CRS_ID = enrollments.CRS_ID  AND classdata.ACAD_TERM_CD = enrollments.ACAD_TERM_CD \
                WHERE 1= 1 "

        sqlCourseDetailViewHeader1 = sqlCourseDetailViewHeader1 +   " AND classdata.CRS_ID = " + courseID + " AND  classdata.ACAD_TERM_CD = " + term + " AND classdata.COI_INST_CD = '"+ CampusOfInstruction + "'" 
        sqlCourseDetailViewHeader1 = sqlCourseDetailViewHeader1 +   " Order By 1 "
        dataHeader1 = dataAdapter.executeOne(sqlCourseDetailViewHeader1)

        # print(sqlCourseDetailViewHeader1)
        # print(dataHeader1)

        sqlCourseDetailViewHeader2 = "Select CRS_ID, ACAD_TERM_CD, COUNT(IF(enrollments.STU_ENRL_STAT_REAS_CD='ENRL',0, NULL)) 'ENRLLOED', \
                    COUNT(IF(enrollments.STU_ENRL_STAT_REAS_CD='DROP',0, NULL)) 'DROP', \
                    COUNT(IF(enrollments.STU_ENRL_STAT_REAS_CD='WDRW',0, NULL)) 'WITHDRAWAL' \
                    from iuie_enrollments enrollments \
                    WHERE enrollments.CRS_ID = " + courseID + " AND  enrollments.ACAD_TERM_CD = '" + term + "'"
        dataHeader2 = dataAdapter.executeOne(sqlCourseDetailViewHeader2)

        # print(sqlCourseDetailViewHeader2)
        # print(dataHeader2)
        
        sqlCourseDetailViewCampusSeats = " SELECT  classdata.COI_INST_CD, classdata.COE_INST_CD, classdata.ENROLLMENT_CAP, \
            classdata.ENROLLMENT_TOTAL, classdata.ENROLLMENT_CAP - classdata.ENROLLMENT_TOTAL 'Calculated Remaining' \
            FROM iuie_classes classdata "

        sqlCourseDetailViewCampusSeats = sqlCourseDetailViewCampusSeats +  " WHERE classdata.CRS_ID = " + courseID + " AND classdata.ACAD_TERM_CD = '" + term + "' AND classdata.COI_INST_CD = '" + CampusOfInstruction + "'"
        sqlCourseDetailViewCampusSeats = sqlCourseDetailViewCampusSeats + " Order By 2 "
        dataCampusSeats = dataAdapter.execute(sqlCourseDetailViewCampusSeats)

        # print(sqlCourseDetailViewCampusSeats)
        # print(dataSectionsSeats)

        sqlCourseDetailViewStudentDetails = "  SELECT  CONCAT(applications.PRSN_PREF_1st_NM, ' ', applications.PRSN_PREF_MID_NM, ' ',applications.PRSN_PREF_LAST_NM) 'Student Name', \
            enrollments.CLS_NBR, enrollments.STU_ENRL_STAT_REAS_CD \
            from iuie_classes classdata \
            left join iuie_enrollments enrollments \
            on classdata.CRS_ID = enrollments.CRS_ID AND classdata.ACAD_TERM_CD = enrollments.ACAD_TERM_CD \
            left join iuie_applications applications \
            on enrollments.PRSN_UNIV_ID  = Trim(leading '0' from applications.PRSN_UNIV_ID) "
        
        sqlCourseDetailViewStudentDetails = sqlCourseDetailViewStudentDetails +  " WHERE classdata.CRS_ID = " + courseID + " AND classdata.ACAD_TERM_CD = '" + term + "' AND classdata.COI_INST_CD = '" + CampusOfInstruction + "'"
        sqlCourseDetailViewStudentDetails = sqlCourseDetailViewStudentDetails +   " group by CONCAT(applications.PRSN_PREF_1st_NM, ' ', applications.PRSN_PREF_MID_NM, ' ',applications.PRSN_PREF_LAST_NM), enrollments.CLS_NBR, enrollments.STU_ENRL_STAT_REAS_CD \
            order By 1 "

        dataStudentDetails = dataAdapter.execute(sqlCourseDetailViewStudentDetails)

        # print(sqlCourseDetailViewStudentDetails)
        # print("--------------------------------------------------------------------------------------------------------------------------")
        # print(dataStudentDetails)
        
        return dataHeader1, dataHeader2, dataCampusSeats, dataStudentDetails

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


    
