# !/usr/bin/env python
# -*- coding:utf-8 -*-
from lib.Dao.DaoMapper import DaoMapper
dao = DaoMapper("spiderconfig")
spiderdao = DaoMapper()
class ProcessorUtil:
    @staticmethod
    def findUnUpdatedList(defaultId,offset,num):
        queryUrl = "SELECT externalEstateId,latitude,longitude FROM external_estate_temp_gaode t where t.isUpdated = 0 ORDER BY citycode asc limit "+ str(offset)+","+str(num)
        print(queryUrl)
        result = spiderdao.operationSql(sql=queryUrl)
        print(result)
        subEstateResult = []
        if result is None:
            pass
        else:
            for tmp in result:
                externalEstateId = tmp[0]
                latitude = tmp[1]
                longitude = tmp[2]
                point = [externalEstateId, latitude, longitude]
                subEstateResult.append(point)
        if len(subEstateResult) == 0:
            subEstateResult.append([defaultId, 0, 0])
        print(subEstateResult)
        return subEstateResult
        pass
    @staticmethod
    def updateListBatch(orderDics):
        import types
        if len(orderDics)<=0:
            return
        updateBatchSql = """ INSERT INTO spider.external_estate_temp_gaode (
	            externalEstateId,townName,cityName,initName,memo,
                completed,greenRate,volumeRate,
                propertyCharges,propertyCompany,developers,
                parkingSpace,propertyRight,shape,isUpdated,latitude,longitude) VALUES """
        end ="""ON DUPLICATE KEY UPDATE
                `townName` = VALUES(`townName`),
                `cityName` = VALUES(`cityName`),
                `initName` = VALUES(`initName`),
                `memo` = VALUES (`memo`),
                `completed` = VALUES(`completed`),
                `greenRate` = VALUES(`greenRate`),
                `volumeRate` = VALUES(`volumeRate`),
                `propertyCharges` = VALUES(`propertyCharges`),
                `propertyCompany` = VALUES (`propertyCompany`),
                `developers` = VALUES(`developers`),
                `parkingSpace` = VALUES(`parkingSpace`),
                `propertyRight` = VALUES(`propertyRight`),
                `shape` = VALUES(`shape`),
                `isUpdated` = VALUES(`isUpdated`),
                `latitude` = VALUES(`latitude`),
                `longitude` = VALUES(`longitude`)"""

        params=""
        for orderDic in orderDics:
            tmp = "("
            for key,value in orderDic.items():
                if key == "memo":
                    value = value.replace("\'","")
                if type(value) == types.StringType or type(value) == types.UnicodeType:
                    tmp +=  ("'" + value + "',")
                else:
                    tmp +=  str(value) + ","
                    pass
            if len(tmp) > 0:
                tmp = tmp[:-1]
            tmp += "),"
            params+=tmp
        if len(params) > 0:
            params = params[:-1]

        updateBatchSql = updateBatchSql+params+end
        print("final sql="+updateBatchSql)
        spiderdao.operationUpdateSql(sql=updateBatchSql.replace('\\','').replace(':','\\:'))
        pass

    @staticmethod
    def findUnUpdatedListAnjuke(defaultId, offset, num):
        queryUrl = "SELECT externalEstateId,note FROM external_estate_temp_anjuke t" \
                   " where t.isUpdated = 0 and t.note is not null ORDER BY cityId asc limit " + str(
            offset) + "," + str(num)

        #queryUrl = "SELECT externalEstateId,note FROM external_estate_temp_anjuke t where t.isUpdated=1 and t.externalEstateId=174414"
        print(queryUrl)
        result = spiderdao.operationSql(sql=queryUrl)
        print("查询结果")
        print(result)
        subEstateResult = []
        if result is None:
            pass
        else:
            for tmp in result:
                cityIndex = tmp[1]
                externalEstateId = tmp[0]
                subEstateResult.append([cityIndex,externalEstateId])
        if len(subEstateResult) == 0:
            subEstateResult.append(["shanghai",defaultId])
        print(subEstateResult)
        return subEstateResult
        pass

    @staticmethod
    def updateAnjukeListBatch(objs):
        import types
        if len(objs) <= 0:
            return
        updateBatchSql = """ INSERT INTO spider.external_estate_temp_anjuke (
        	            externalEstateId,pageUrl,latitude,longitude,propertyType,propertyCharges,
                        floorArea,totalHouse,parkingLot,
                        volumeRate,greenRate,propertyCompany,
                        developers,memo,isUpdated) VALUES """
        end = """ON DUPLICATE KEY UPDATE
                        `externalEstateId` = VALUES(`externalEstateId`),
                        `pageUrl` = VALUES(`pageUrl`),
                        `latitude` = VALUES(`latitude`),
                        `longitude` = VALUES(`longitude`),
                        `propertyType` = VALUES (`propertyType`),
                        `propertyCharges` = VALUES(`propertyCharges`),
                        `floorArea` = VALUES(`floorArea`),
                        `totalHouse` = VALUES(`totalHouse`),
                        `parkingLot` = VALUES(`parkingLot`),
                        `volumeRate` = VALUES (`volumeRate`),
                        `greenRate` = VALUES(`greenRate`),
                        `propertyCompany` = VALUES(`propertyCompany`),
                        `developers` = VALUES(`developers`),
                        `memo` = VALUES(`memo`),
                        `isUpdated` = VALUES(`isUpdated`)
                         """

        params = ""
        for orderDic in objs:
            tmp = "("
            for key, value in orderDic.items():
                if key == "memo":
                    value = value.replace("\'", "")
                if type(value) == types.StringType or type(value) == types.UnicodeType:
                    tmp += ("'" + value + "',")
                else:
                    tmp += str(value) + ","
                    pass
            if len(tmp) > 0:
                tmp = tmp[:-1]
            tmp += "),"
            params += tmp
        if len(params) > 0:
            params = params[:-1]

        updateBatchSql = updateBatchSql + params + end
        print("final sql=" + updateBatchSql)
        spiderdao.operationUpdateSql(sql=updateBatchSql.replace('\\', '').replace(':', '\\:'))
    @staticmethod
    def updateAnjukeImageBatch(objs):
        import types
        if len(objs) <= 0:
            return
        updateBatchSql = """ INSERT INTO spider.external_estate_image_temp_anjuke (
                	            externalEstateId,externalImgUrl,status) VALUES """
        end = """ON DUPLICATE KEY UPDATE
                                `externalEstateId` = VALUES(`externalEstateId`),
                                `externalImgUrl` = VALUES(`externalImgUrl`),
                                `status` = VALUES(`status`)"""

        params = ""
        for orderDic in objs:
            tmp = "("
            for key, value in orderDic.items():
                if key == "memo":
                    value = value.replace("\'", "")
                if type(value) == types.StringType or type(value) == types.UnicodeType:
                    tmp += ("'" + value + "',")
                else:
                    tmp += str(value) + ","
                    pass
            if len(tmp) > 0:
                tmp = tmp[:-1]
            tmp += "),"
            params += tmp
        if len(params) > 0:
            params = params[:-1]

        updateBatchSql = updateBatchSql + params + end
        print("final sql=" + updateBatchSql)
        spiderdao.operationUpdateSql(sql=updateBatchSql.replace('\\', '').replace(':', '\\:'))
        pass
    @staticmethod
    def parseByXPath(etree, path):
        xpath = etree.xpath(path)
        if len(xpath) > 0:
            result = xpath[0]
        else:
            result = ""
        return result