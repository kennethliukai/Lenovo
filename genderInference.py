# -*- coding: utf-8 -*-
'''
Process the apppackage_name
'''
import sys
import numpy as np
import time
import pp
reload(sys)
sys.setdefaultencoding('utf-8')

def appClasses(appClass):
    fr = open('apppackage_name')
    fw = open(appClass+'apps.txt', 'w')
    #dataMat = []
    for line in fr.readlines():
        line = line.encode('utf-8')
        if (line.find(appClass) != -1):
            fw.write('%s' %line)
        #curLine = line.strip().split(',')
        #fltLine = map(float,curLine) #map all elements to float()
        #dataMat.append(curLine)
    fr.close()
    fw.close()

#Find the group of apps, the name of groups are the last two keywords of the app name
#Find the apps in each group
def appGroupsDict(appFile):
    start_time = time.time()
    fr = open(appFile)
    fw = open('appGroups', 'w')
    groupList = []
    appList = []
    #find the group list
    for line in fr.readlines():
        line = line.encode('utf-8')
        curLine = line.strip().split(',')
        s = curLine[-3]+','+curLine[-2]
        if not s in groupList:
            groupList.append(s)
        appList.append(line)
    print "group list found \n"
    #find the apps in each group, using dictionary, the key is the group name
    #value is the list of apps in this group
    groupDict = {}
    for group in groupList:
        group = group.encode('utf-8')
        for line in appList:
            line = line.encode('utf-8')
            if (line.find(group) != -1):
                app = line.strip().split(',')
                appID = app[0]
                if not groupDict.has_key(group):
                    groupDict[group] = [appID]
                else:
                    groupDict[group].append(appID)
    fw.write('%s'%groupDict)
    print "group dictionary found and is written to file"
    print "Time elapsed: ", time.time()-start_time,"s"
    fr.close()
    fw.close() 
    return groupDict

def deleteDuplicate(filename):
    fr = open(filename)
    fw = open(filename+'NoDuplicate.txt','w')
    lines = []
    for line in fr.readlines():
        line = line.encode('utf-8')
        if not line in lines:
            lines.append(line)
            fw.write('%s'%line)
    fr.close()
    fw.close()
    
def userGroupMatrix():
    
    start_time = time.time()
    fr = open('apppackage_name')
    fir = open('install_log_00')
    groupList = []
    appList = []
    
    #find the group list
    for line in fr.readlines():
        line = line.encode('utf-8')
        curLine = line.strip().split(',')
        s = curLine[-3]+','+curLine[-2]
        if not s in groupList:
            groupList.append(s)
        appList.append(line)
    print "group list found \n"
    #find the apps in each group, using dictionary, the key is the group name
    #value is the list of apps in this group
    groupDict = {}
    for group in groupList:
        group = group.encode('utf-8')
        for line in appList:
            line = line.encode('utf-8')
            if (line.find(group) != -1):
                app = line.strip().split(',')
                appID = app[0]
                if not groupDict.has_key(group):
                    groupDict[group] = [appID]
                else:
                    groupDict[group].append(appID)
        
    print "group dictionary found "
    print "Time elapsed: ", time.time()-start_time,"s"
    #userInstallDict give the installed apps for each user, key is the user ID
    #value is the list of apps he/she installed
    
    userInstallDict = {}
    for installEvent in fir.readlines():
        curEvent = installEvent.strip().split(',')
        user = curEvent[0]
        app = curEvent[1]
        if not userInstallDict.has_key(user):
            userInstallDict[user] = [app]
        else:
            userInstallDict[user].append(app)
    userList = userInstallDict.keys()
    numUsers = len(userList)
    numGroups = len(groupList)
    print "user install dictionary found"
    print "Time elapsed: ", time.time()-start_time,"s"
    #userGroupMatrix give the distributions of installed apps in each group for each user
    userGroupMatrix = np.mat(np.zeros((numUsers,numGroups)))
    for i in range(numUsers):
        for j in range(numGroups): 
            count = 0
            for appInstalled in userInstallDict[userList[i]]:    
                #第j个group的app里面是否有第i个user安装过的app，有一个count加1           
                if appInstalled in groupDict[groupList[j]]:
                    count =count +1
            userGroupMatrix[i,j] = count           
         
    fr.close()
    fir.close()
    print "User group matrix built"
    print "Time elapsed: ",time.time()-start_time,"s"
    return userGroupMatrix

def userAppDict(install_log):
    start_time = time.time()
    fr = open(install_log)
    fw = open(install_log+'Dict','w')
    userInstallDict = {}
    for installEvent in fr.readlines():
        curEvent = installEvent.strip().split(',')
        user = curEvent[0]
        app = curEvent[1]
        if not userInstallDict.has_key(user):
            userInstallDict[user] = [app]
        else:
            userInstallDict[user].append(app)
    fw.write("%s" %userInstallDict)
    fr.close()
    fw.close()
    print "Time elapsed for user install: ",time.time()-start_time,"s"
    return userInstallDict

#find labeled users. classify if a user is male or female. based on the relative statistics of the male-specific apps and female-specific apps he/she installed    
def appGender(appFile):
    start_time = time.time()
    fr = open(appFile)
    maleAppClass = [u'动作游戏',u'射击游戏',u'美女',u'彩票',u'男生',u'男士',u'男性',u'电子市场',\
    u'足球',u'篮球',u'NBA',u'英雄联盟']
    femaleAppClass = [u'音乐游戏',u'养成游戏',u'儿童教育',u'女性',u'女生',u'女士',u'女人',u'幼儿教育',u'星座',u'爱情',u'瑜伽',\
            u'网购',u'美化',u'美图',u'美容',u'化妆',u'美甲',u'宝宝',u'宝贝',u'食谱',\
            u'育儿',u'蘑菇街',u'妈妈',u'妈咪',u'孕',u'八卦',u'聚美优品',u'儿童']

    fwm = open('maleApps','w')
    fwf = open('femaleApps','w')
    
    #这样会出现重复的项，比如一个app符合一个以上的类，就会被写入多次（这个问题，用break解决，甚至同时包括了男性和女性的类，就会
    #同时出现在maleApps和femaleApps里面。解决方法是，如果同时在男性和女性，这个apps就不当做性别化强的app来用
    #从apppackage_name 里读取一行，看该行是否属于男性类别（符合男性类别任何一个关键字就可以），如果在，male被置成1，如果不在
    #继续看是否在女性类别里，如果在，female被置成1.最好判断是否该被当作男性app还是女性app或者都不是。
    maleList = []
    femaleList = []
    for line in fr.readlines():
        line = line.encode('utf-8')
	curLine = line.strip().split(',')
	appID = curLine[0]
        male = 0
        female = 0
        for appClass in maleAppClass:
            if (line.find(appClass) != -1):
                male = 1
                break
        for appClass in femaleAppClass:
            if (line.find(appClass) != -1):
                female = 1
                break
        if male==1 and female==0:
	    maleList.append(appID)
            fwm.write('%s' %line)
        if female==1 and male==0:
	    femaleList.append(appID)
            fwf.write('%s' %line)
    print "Time slapsed for gender-specific apps: ",time.time()-start_time,"s"

    
            
    fr.close()
    fwm.close()
    fwf.close()
    return maleList,femaleList
    
def labelUsers(userInstallDict,maleList,femaleList):
	fwm = open('maleUsers','w')
	fwf = open('femaleUsers','w')
	fw1 = open('userGenderList','w')
	numOfUsers = len(userInstallDict)
	userGenderDict = {}
	maleUserList = []
	femaleUserList = []
	for (k,v) in userInstallDict.items():
		countMaleApps = 0
		countFemaleApps = 0
		for app in v:
			if app in maleList:
				countMaleApps +=1
			elif app in femaleList:
				countFemaleApps +=1
		if (countMaleApps>0 or countFemaleApps>0):
			diff = (float(countMaleApps)-float(countFemaleApps))/(countMaleApps + countFemaleApps)
			if (diff>0 and diff<=1.0):
				userGenderDict[k] = ['male',countMaleApps,countFemaleApps]
				maleUserList.append(k)
				print "%s" %k,userGenderDict[k]
				fwm.write("%s:%s\n"%(k,userGenderDict[k]))
			elif (diff<0 and diff>=-1.0):
				userGenderDict[k] = ['female',countMaleApps,countFemaleApps]
				femaleUserList.append(k)
				print "%s"%k,userGenderDict[k]
				fwf.write("%s:%s\n"%(k,userGenderDict[k]))
	print "number of male/female users: ",len(maleUserList),"\t",len(femaleUserList)	
	fw1.write("users labeled as male: \n%s"%maleUserList,"female: \n%s"%femaleUserList)
	fwm.close()
	fwf.close()
	fw1.close()
	return userGenderDict,maleUserList,femaleUserList

    
def labelSingleUser(user,installedAppList,maleList,femaleList):
    userGender = []
    countMaleApps = 0
    countFemaleApps = 0
    for app in installedAppList:
		if app in maleList:
			countMaleApps +=1
		elif app in femaleList:
			countFemaleApps +=1
    if (countMaleApps>0 or countFemaleApps>0):
		relative_diff = (float(countMaleApps)-float(countFemaleApps))/(countMaleApps + countFemaleApps)
		if (relative_diff>0 and relative_diff<=1.0):
			userGender = ['male',countMaleApps,countFemaleApps]
			print "user %s"%user, "is", userGender
		elif (relative_diff<0 and relative_diff>=-1.0):
			userGender = ['female',countMaleApps,countFemaleApps]
			print "user %s"%user, "is", userGender
    return userGender

def readGenderApps(maleFile,femaleFile):
	frm = open(maleFile)
	frf = open(femaleFile)
	maleList = []
	femaleList = []
	for line in frm.readlines():
		curLine = line.strip().split(',')
		maleList.append(curLine[0])
	for line in frf.readlines():
		curLine = line.strip().split(',')
		femaleList.append(curLine[0])
	frm.close()
	frf.close()
	return maleList,femaleList
	
def readUserAppDict(install_log_dict):
	fr = open(install_log_dict)
	userInstallDict = {}
	for line in fr.readlines():
		curLine = line.strip().split(',')		
		userInstallDict[curLine[0]] = [value for value in curLine[1:-1]]
	return userInstallDict
def test():
	print "testing"
	fwresult = open('result','w')
	maleList,femaleList = readGenderApps('test_male_apps','test_female_apps')
	userInstallDict = readUserAppDict('test_install_log_dict')
	
	for user in userInstallDict.keys():    
		# job = job_server.submit(labelSingleUser, (userInstallDict[user],maleList,femaleList,))
		result = labelSingleUser(userInstallDict[user],maleList,femaleList)
		# #print "parallel result: user %s"%user, "is", job()
		print "user %s"%user, "is", result
		# #fwresult.write("user %s is %s \n" %(user,job()))
		fwresult.write("user %s is %s \n" %(user,result))

def parallelInference(userInstallDict,maleList,femaleList,ncpus=0):
	print """ncpus - the number of workers to run in parallel, 
		if omitted it will be set to the number of processors in the system
		"""
		
	userList = userInstallDict.keys()
	userGenderDict = {}
	numUsers = len(userList)
	# tuple of all parallel python servers to connect with
	ppservers = ()
	#ppservers = ("10.0.0.1",)
	if ncpus > 0:		
		# Creates jobserver with ncpus workers
		job_server = pp.Server(ncpus, ppservers=ppservers)
	else:
		# Creates jobserver with automatically detected number of workers
		job_server = pp.Server(ppservers=ppservers)
		ncpus = job_server.get_ncpus()
	print "Starting pp with ", ncpus, " workers"
	# Submit a job of calulating userGender for execution. 
	# userGender - the function
	# (installedAppList,maleList,femaleList,) - tuple with arguments for userGender
	# (isprime,) - tuple with functions on which function sum_primes depends
	# ("math",) - tuple with module names which must be imported before sum_primes execution
	# Execution starts as soon as one of the workers will become available
	fwresult = open('result_parallel'+str(time.time()),'w')
	#job1 = job_server.submit(labelSingleUser, (userInstallDict[k],maleList,femaleList,))
	# Retrieves the result calculated by job1
	# If the job has not been finished yet, execution will wait here until result is available
	#result = job1()
	#userGenderDict[k] = result
	#fwresult.write( "user %s is %s " %(k,result))
	#print "user %s"%k," is %s " %result
	start_time = time.time()
	# The following submits 8 jobs and then retrieves the results
	#inputs = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700)
	jobs = [(user, job_server.submit(labelSingleUser,(user,userInstallDict[user],maleList,femaleList,))) for user in userInstallDict.keys()]
	for user,job in jobs:    
		#job = job_server.submit(labelSingleUser, (userInstallDict[user],maleList,femaleList,))
		#result = labelSingleUser(userInstallDict[user],maleList,femaleList)
		result = job()
		if result:
			print "parallel result: user %s"%user, "is", result
			#print "user %s"%user, "is", result
			fwresult.write("parallel result: user %s is %s \n" %(user,result))
			#fwresult.write("user %s is %s \n" %(user,result))
	print "Time elapsed for parallel labelling data ", time.time() - start_time, "s"
	fwresult.close()
	job_server.print_stats()

def nonParallelInference(userInstallDict,maleList,femaleList):
	
	fwresult = open('result'+str(time.time()),'w')
	start_time = time.time()
	userList = userInstallDict.keys()
	userGenderDict = {}
	numUsers = len(userList)
	for user in userList:
		result = labelSingleUser(user,userInstallDict[user],maleList,femaleList)
		if result:
			print "user %s"%user, "is", result
			fwresult.write("%s:%s \n" %(user,result))
	print "Time elapsed for labelling data: ", time.time() - start_time, "s"
	fwresult.close()


maleList,femaleList = appGender('apppackage_name')
userInstallDict = userAppDict('install_log')
labelUsers(userInstallDict,maleList,femaleList)

# if len(sys.argv) > 1:
    # ncpus = int(sys.argv[1])
    # parallelInference(userInstallDict,maleList,femaleList,ncpus)
# else:
	# nonParallelInference(userInstallDict,maleList,femaleList)