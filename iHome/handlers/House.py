#coding：utf-8
import logging

from .BaseHandler import BaseHandler
from utils.common import require_logined
from utils.response_code import RET

class HouseInfoHandler(BaseHandler):
    """房屋信息"""
    @require_logined
    def post(self):
        """上传"""
        user_id = self.session.data.get("user_id")
        title = self.json_args.get("title")
        price = self.json_args.get("price")
        area_id = self.json_args.get("area_id")
        address = self.json_args.get("address")
        room_count = self.json_args.get("room_count")
        acreage = self.json_args.get("acreage")
        unit = self.json_args.get("unit")
        capacity = self.json_args.get("capacity")
        beds = self.json_args.get("beds")
        deposit = self.json_args.get("deposit")
        min_days = self.json_args.get("min_days")
        max_days = self.json_args.get("max_days")
        facility = self.json_args.get("facility")

        if not all((title,price,area_id,address,room_count,acreage,unit,capacity,beds,deposit,min_days,max_days,facility)):
            return  self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))
        try:
            ret = self.db.execute("insert into ih_house_info(hi_user_id,hi_title,hi_price,hi_area_id,hi_address,hi_room_count,hi_acreage,hi_house_unit,hi_capacity,hi_beds,hi_deposit,hi_min_days,hi_max_days) values(%(user_id)s,%(title)s,%(price)s,%(ares_id)s,%(address)s,%(room_count)s,%(acreage)s,%(house_unit)s,%(capacity)s,%(beds)s,%(deposit)s,%(min_days)s,%(max_days)s)",user_id=user_id,title=title,price=price,area_id=area_id,address=address,room_count=room_count,acreage=acreage,house_unit= unit,capacity=capacity,beds=beds,deposit=deposit,min_days=min_days,max_days=max_days)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.DEERR, errmsg="保存数据错误"))
        try:
