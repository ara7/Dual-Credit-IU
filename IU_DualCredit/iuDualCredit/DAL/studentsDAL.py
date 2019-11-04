from DAL import dataAdapter


def campusList():

    try:
    
        sqlCampusList = "SELECT Distinct applications.INST_CD FROM  iuie_applications applications Order By 1 " 
        data = dataAdapter.execute(sqlCampusList)
        CampusList = dataAdapter.ConvertToList(data, 0)    
        return CampusList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)




def dcPartnerList():


    try:
        sqldcPartnerList = "SELECT Distinct Institution FROM iuie_qualitrics_data Where Institution <> '' Order By 1 " 
        data = dataAdapter.execute(sqldcPartnerList)
        dcPartnerList = dataAdapter.ConvertToList(data, 0)    
        return dcPartnerList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


    



def studentsList(userName, UID, firstName, lastName, campusOfEnrollment, dcPartner, currentlyEnrolled):
    

    try:

        sqlStudentQuery = " SELECT Distinct Trim(leading '0' from applications.PRSN_UNIV_ID), Concat(PRSN_PREF_1ST_NM,' ', PRSN_PREF_MID_NM, ' ',  PRSN_PREF_LAST_NM) 'Student Name', \
                        qualitricsData.Institution, qualitricsData.Spring_CourseFirstRequest, qualitricsData.Spring_CourseSecondRequest, \
                        CREDITS_COMPLETED, PRSN_GDS_CMP_EMAIL_ADDR, INST_CD \
                        from iuie_applications applications \
                        Left Join iuie_qualitrics_data qualitricsData \
                        on Trim(leading '0' from applications.PRSN_UNIV_ID)  = qualitricsData.Student_UID \
                        Left join iuie_enrollments enrollments \
                        on Trim(leading '0' from applications.PRSN_UNIV_ID)  = enrollments.PRSN_UNIV_ID \
                        Where 1 = 1 " 
    
        if userName:
            sqlStudentQuery = sqlStudentQuery + " AND Lower(applications.PRSN_NTWRK_ID) Like Lower('%" + userName + "%') "

        if UID:
            sqlStudentQuery = sqlStudentQuery + " AND Lower(applications.PRSN_UNIV_ID) Like ('%" + UID + "%')"

        if firstName:
            sqlStudentQuery = sqlStudentQuery + " AND ( Lower(applications.PRSN_PREF_1st_NM) Like Lower('%" + firstName + "%') OR Lower(applications.PRSN_PREF_MID_NM) Like Lower('%" + firstName + "%') ) "

        if lastName:
            sqlStudentQuery = sqlStudentQuery + " AND Lower(applications.PRSN_PREF_LAST_NM) Like Lower('%" + lastName + "%')"

        if campusOfEnrollment:
            sqlStudentQuery = sqlStudentQuery + " AND Lower(applications.INST_CD) = Lower('" + campusOfEnrollment + "')"

        if dcPartner:
            sqlStudentQuery = sqlStudentQuery + " AND Lower(qualitricsData.Institution) = Lower('" + dcPartner + "')"

        if (currentlyEnrolled == "true"):
            sqlStudentQuery = sqlStudentQuery + " AND enrollments.STU_ENRL_STAT_REAS_CD = 'ENRL' "

        sqlStudentQuery = sqlStudentQuery + " Order by 1 "

        ## Important
        # if studentType:
        #     sqlCoursesQuery = sqlCoursesQuery + " AND Lower(applications.INST_CD) = Lower('" + studentType + "')"
        # if pendingEnrollmentRequests:
        #         sqlCoursesQuery = sqlCoursesQuery + " AND applications.ACAD_TERM_CD = '" + pendingEnrollmentRequests + "'"
        # print(sqlStudentQuery)

        data = dataAdapter.execute(sqlStudentQuery)
        # print(data)
        
        return data

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)



    


def studentDetailView(UID):    
    

    try:
        # Student Details
        sqlStudentDetails = " SELECT DISTINCT Concat(PRSN_PREF_1ST_NM,' ', PRSN_PREF_MID_NM, ' ',  PRSN_PREF_LAST_NM) 'Student Name', \
                            PRSN_NTWRK_ID, Trim(leading '0' from applications.PRSN_UNIV_ID), \
                            DATE_FORMAT(PRSN_BIRTH_DT,'%b %d %Y') 'Birth Date',  \
                            qualitricsData.legal_sex, qualitricsData.OPTIONAL_GenderIdentity, qualitricsData.Primary_PhoneNumber, qualitricsData.Contact_Method, qualitricsData.Student_PrimaryEmailAddress, \
                            Concat(CurrentAddress_Street, ' ', CurrentAddress_City, ' ', CurrentAddress_State, ' ', CurrentAddress_PostalCode , ' ', CurrentAddress_Country , ' '),  \
                            Concat(PermanentMailingAddress_Street, ' ', PermanentMailingAddress_City, ' ', PermanentMailingAddress_State, ' ', PermanentMailingAddress_PostalCode , ' ', PermanentMailingAddress_Country , ' '), \
                            qualitricsData.US_Status, Documents_Arrived_UnderAnyOtherName \
                            FROM iuie_applications applications  \
                            Left Join iuie_qualitrics_data qualitricsData \
                            on Trim(leading '0' from applications.PRSN_UNIV_ID)  = qualitricsData.Student_UID \
                            Where Trim(leading '0' from applications.PRSN_UNIV_ID) = '"  + UID + "' LIMIT 1 "

        dataStudentDetails = dataAdapter.executeOne(sqlStudentDetails)
        # print(sqlStudentDetails)


        # Former Names
        sqlStudentFormerNames = " SELECT FormerNames1  'FormerName' \
                                    from iuie_qualitrics_data qualitricsData \
                                    where qualitricsData.Student_UID = Trim(leading '0' from '" + UID + "') \
                                    union \
                                    SELECT FormerNames2 \
                                    from iuie_qualitrics_data qualitricsData \
                                    where qualitricsData.Student_UID = Trim(leading '0' from '" + UID + "') \
                                    union \
                                    SELECT FormerNames3  \
                                    from iuie_qualitrics_data qualitricsData \
                                    where qualitricsData.Student_UID = Trim(leading '0' from '" + UID + "') \
                                    union \
                                    SELECT FormerNames4 \
                                    from iuie_qualitrics_data qualitricsData \
                                    where qualitricsData.Student_UID = Trim(leading '0' from '" + UID + "') \
                                    union \
                                    SELECT FormerNames5 \
                                    from iuie_qualitrics_data qualitricsData \
                                    where qualitricsData.Student_UID = Trim(leading '0' from '" + UID + "') \
                                    Order By 1 desc "    
        
        dataStudentFormerNames = dataAdapter.execute(sqlStudentFormerNames)
        
        ListStudentFormerNames = []
        for formerNames in dataStudentFormerNames:
            for formerName in formerNames:
                ListStudentFormerNames.append(formerName)
        
        #print(sqlStudentFormerNames)
    
        # Qualitrics Tabs
        sqlStudentQualitricsTabsHeader = "Select Distinct acadterm.acad_term_cd, acadterm.acad_term  \
                                            from iuie_qualitrics_data qualitricsData  \
                                            Inner Join iuie_academic_terms acadterm \
                                            on qualitricsData.Acadmic_Term = acadterm.acad_term \
                                            Where qualitricsData.Student_UID = Trim(leading '0' from '" + UID + "') Order By 1 "
        
        # print(sqlStudentQualitricsTabsHeader)
        
        dataStudentQualitricsTabsHeader = dataAdapter.execute(sqlStudentQualitricsTabsHeader)
        
        # print(sqlStudentQualitricsTabsHeader)
        # print(dataStudentQualitricsTabsHeader)
        
        # Qualitric Data
        # sqlStudentQualitricsTabsData = " "
        # dataStudentQualitricsTabsData = dataAdapter.execute(sqlStudentQualitricsTabsData)

        # Enrollment History Data
        sqlStudentEnrollmentHistory = "Select Distinct enrollments.CRS_DESC, enrollments.CLS_NBR, acadterm.acad_term, enrollments.STU_ENRL_STAT_REAS_CD, \
                                        enrollments.CRS_OFCL_GRD_CD, applications.CREDITS_COMPLETED \
                                        from iuie_enrollments enrollments \
                                        Left Join iuie_classes classdata \
                                        on classdata.CRS_ID = enrollments.CRS_ID AND classdata.ACAD_TERM_CD = enrollments.ACAD_TERM_CD \
                                        Left Join iuie_applications applications \
                                        on enrollments.PRSN_UNIV_ID  = Trim(leading '0' from applications.PRSN_UNIV_ID) \
                                        Left Join iuie_academic_terms acadterm \
                                        on enrollments.ACAD_TERM_CD = acadterm.acad_term_cd \
                                        Where enrollments.PRSN_UNIV_ID = Trim(leading '0' from '" + UID + "') \
                                        Order By 2,3 " 

        dataStudentEnrollmentHistory = dataAdapter.execute(sqlStudentEnrollmentHistory)
        
        # print(sqlStudentEnrollmentHistory)

        # Course Request
        sqlStudentCourseRequest =  "Select enrollments.STU_ENRL_ADD_DT,  enrollments.CRS_ID, enrollments.CLS_NBR, enrollments.STU_ENRL_DRP_DT \
                                    from iuie_enrollments enrollments \
                                    Where enrollments.PRSN_UNIV_ID = Trim(leading '0' from '" + UID + "')"

        dataStudentCourseRequest = dataAdapter.execute(sqlStudentCourseRequest)
        
        # Comments
        # sqlStudentCommentsData = " "
        # dataStudentCommentsData = dataAdapter.execute(sqlStudentCommentsData)
        
        return dataStudentDetails, ListStudentFormerNames, dataStudentQualitricsTabsHeader, dataStudentEnrollmentHistory, dataStudentCourseRequest

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)



 


def studentYearWiseQualitricsData(UID, academicYear): 
    # Change the Query

    # print(UID)
    # print(academicYear)

    try:
        sqlStudentQualitricsData = " Select Response_ID, End_Date, Concat(Start_Date, ' - ', End_Date),  \
                                 Case When role_Description = 'I am an instructor in Indiana Universityâ€™s Advance College Project (ACP).' Then 'IU' \
                                 ELSE Concat(Institution,' - ', High_School) \
                                 END AS 'DC Partner', MoreThan_TwoYears_TeachingExperience, \
                                 StateLicensure, Class_Taken_IndianaUniversity, FullLegalName \
                                 From iuie_qualitrics_data qualitricsData \
                                 Left Join iuie_academic_terms acadterm \
                                 on qualitricsData.Acadmic_Term = acadterm.acad_term \
                                 Where Student_UID = Trim(leading '0' from '" + UID + "') ANd acadterm.acad_term_cd = '"+ academicYear +"'  \
                                 Order by 1 "
    
        #print(sqlStudentQualitricsData)

        dataStudentQualitricsData = dataAdapter.execute(sqlStudentQualitricsData)
        
        #StudentQualitricsYearDataList = dataAdapter.ConvertToList(dataStudentQualitricsData, 0)    

        return dataStudentQualitricsData


    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)




