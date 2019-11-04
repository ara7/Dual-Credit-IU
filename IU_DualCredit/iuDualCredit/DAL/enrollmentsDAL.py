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


def GetAcadTermCode(term):

    try:

        sqlAcadTermCd = "SELECT acad_term_cd \
                    FROM iuie_academic_terms acadterm \
                    Where 1 = 1 "
        if term:
            sqlAcadTermCd = sqlAcadTermCd + " AND acadterm.acad_term Like ('%" + term + "%')"

        data = dataAdapter.execute(sqlAcadTermCd)
        academicTermCode = dataAdapter.ConvertToList(data,0) 
        return academicTermCode[0]

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)



    



def courseList():
    try:

        sqlCourseList = "SELECT DISTINCT enrollments.CRS_SUBJ_CD, CONCAT(enrollments.CRS_SUBJ_CD,':', enrollments.CRS_CATLG_NBR) \
                    FROM iuie_enrollments enrollments \
                    Order By 1"; 
        data = dataAdapter.execute(sqlCourseList)
        crsList = dataAdapter.ConvertToList(data,1) 
        return crsList

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)


    


def fundingList():

    try:

        sqlFundingList = "SELECT DISTINCT fundingType \
                    FROM iuie_funding_type Order By 1"; 
        data = dataAdapter.execute(sqlFundingList)
        fundingLst = dataAdapter.ConvertToList(data,0) 
        return fundingLst

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)





def GetFundingId(fundingType):


    try:

        sqlFundingId = "SELECT id \
                    FROM iuie_funding_type  \
                    Where 1 = 1 "

        sqlFundingId = sqlFundingId + " AND fundingType = '" + fundingType + "'"

        #print(sqlFundingId)
        
        data = dataAdapter.execute(sqlFundingId)
        fundingId = dataAdapter.ConvertToList(data,0) 
        return fundingId[0]

    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)



def enrollmentList(term, course, funding):
    

    try:

        if course:
            crsSubjCd = (course.split(':')[0]).strip()
            CrsCatlgNbr = (course.split(':')[1]).strip()

        sqlEnrollmentQuery = "SELECT acadterm.acad_term, CONCAT(enrollments.CRS_SUBJ_CD, ':' ,enrollments.CRS_CATLG_NBR), \
                            date_format(enrollments.STu_ENRL_ADD_DT, '%M %D %Y'), applications.PRSN_NTWRK_ID,  \
                            enrollments.ACAD_TERM_CD, funding_type.fundingtype \
                            from iuie_enrollments enrollments   \
                            Left Join iuie_academic_terms acadterm \
                            on enrollments.ACAD_TERM_CD = acadterm.acad_term_cd \
                            Left Join iuie_applications applications \
                            on enrollments.PRSN_UNIV_ID  = Trim(leading '0' from applications.PRSN_UNIV_ID) \
                            Left Join iuie_grant_enrollment grantEnrollment \
                            on enrollments.PRSN_UNIV_ID = grantEnrollment.PRSN_UNIV_ID \
                            Left Join iuie_funding_type funding_type \
                            on grantEnrollment.grant_id = funding_type.id \
                            Where 1 = 1 "
        
        if term:
            sqlEnrollmentQuery = sqlEnrollmentQuery + " AND enrollments.ACAD_TERM_CD = " + term 
        if course:
            sqlEnrollmentQuery = sqlEnrollmentQuery + " AND enrollments.CRS_SUBJ_CD = '" + crsSubjCd + "' AND enrollments.CRS_CATLG_NBR = '" + CrsCatlgNbr + "'"
        if funding:
            sqlEnrollmentQuery = sqlEnrollmentQuery + " AND grantEnrollment.grant_id = " + str(funding) 

        sqlEnrollmentQuery = sqlEnrollmentQuery + " Order by 5 ASC"

        #print(sqlEnrollmentQuery)

        data = dataAdapter.execute(sqlEnrollmentQuery)

        return data
    
    except:
        error = "Date: " + str(datetime.now()) +  " Error: " +  str(sys.exc_info())
        logging.write_log(error)



