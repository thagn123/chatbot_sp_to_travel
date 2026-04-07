import json
import os
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from langchain_core.tools import tool

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATABASE_DIR = "database"

def load_db(filename: str) -> List[Dict[str, Any]]:
    path = os.path.join(DATABASE_DIR, filename)
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        logger.error(f"Error loading database {filename}: {e}")
    return []

@tool
def search_flights(origin: str, destination: str, date: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai địa điểm.
    Args:
        origin: Điểm khởi hành (ví dụ: 'Hà Nội')
        destination: Điểm đến (ví dụ: 'Đà Nẵng')
        date: Ngày đi (ví dụ: '2024-12-20')
    """
    logger.info(f"Tool search_flights called: {origin} -> {destination} on {date}")
    try:
        flights = load_db("flights.json")
        # Filter by origin and destination (case insensitive)
        results = [
            f for f in flights 
            if f["origin"].lower() == origin.lower() and f["destination"].lower() == destination.lower()
        ]
        
        if not results:
            return json.dumps({
                "success": True,
                "results": [],
                "message": f"Không tìm thấy chuyến bay nào từ {origin} đến {destination}."
            }, ensure_ascii=False)

        return json.dumps({
            "success": True,
            "results": results,
            "context": f"Flights from {origin} to {destination} on {date}"
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in search_flights: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

@tool
def search_hotels(location: str, max_price: float) -> str:
    """
    Tìm kiếm khách sạn tại một địa điểm với mức giá tối đa.
    Args:
        location: Địa điểm tìm khách sạn
        max_price: Giá tối đa cho một đêm (VND)
    """
    logger.info(f"Tool search_hotels called: {location}, max_price: {max_price}")
    try:
        hotels = load_db("hotels.json")
        results = [
            h for h in hotels 
            if h["location"].lower() == location.lower() and h["price"] <= max_price
        ]
        
        if not results:
            return json.dumps({
                "success": True,
                "results": [],
                "message": f"Không tìm thấy khách sạn nào tại {location} với giá dưới {max_price} VND."
            }, ensure_ascii=False)

        return json.dumps({
            "success": True,
            "results": results,
            "context": f"Hotels in {location} under {max_price} VND"
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in search_hotels: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

@tool
def calculate_budget(total_budget: float, expenses: List[float]) -> str:
    """
    Tính toán ngân sách còn lại.
    Args:
        total_budget: Tổng ngân sách ban đầu (VND)
        expenses: Danh sách các khoản chi phí đã tiêu (VND)
    """
    logger.info(f"Tool calculate_budget called: total={total_budget}, expenses={expenses}")
    try:
        total_spent = sum(expenses)
        remaining = total_budget - total_spent
        return json.dumps({
            "success": True,
            "total_budget": total_budget,
            "total_spent": total_spent,
            "remaining_budget": remaining
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in calculate_budget: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

@tool
def search_restaurants(location: str, max_price: float) -> str:
    """
    Tìm kiếm nhà hàng/quán ăn tại một địa điểm theo ngân sách.
    Args:
        location: Địa điểm (ví dụ: 'Đà Nẵng')
        max_price: Mức giá tối đa trên một người (VND)
    """
    logger.info(f"Tool search_restaurants called: {location}, max_price: {max_price}")
    try:
        restaurants = load_db("restaurants.json")
        results = [
            r for r in restaurants 
            if r["location"].lower() == location.lower() and r["price_per_person"] <= max_price
        ]
        
        if not results:
            return json.dumps({
                "success": True,
                "results": [],
                "message": f"Không tìm thấy nhà hàng nào tại {location} với giá dưới {max_price} VND/người."
            }, ensure_ascii=False)

        return json.dumps({
            "success": True,
            "results": results,
            "context": f"Restaurants in {location} under {max_price} VND/person"
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in search_restaurants: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

@tool
def search_attractions(location: str) -> str:
    """
    Tìm kiếm các địa điểm vui chơi, tham quan tại một thành phố.
    Args:
        location: Địa điểm (ví dụ: 'Đà Lạt')
    """
    logger.info(f"Tool search_attractions called: {location}")
    try:
        attractions = load_db("attractions.json")
        results = [
            a for a in attractions 
            if a["location"].lower() == location.lower()
        ]
        
        if not results:
            return json.dumps({
                "success": True,
                "results": [],
                "message": f"Không tìm thấy điểm tham quan nào tại {location}."
            }, ensure_ascii=False)

        return json.dumps({
            "success": True,
            "results": results,
            "context": f"Attractions in {location}"
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in search_attractions: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

@tool
def get_current_datetime() -> str:
    """
    Truy xuất ngày và giờ hiện tại.
    Công cụ này hữu ích khi người dùng hỏi các câu liên quan đến "hôm nay", "ngày mai", "cuối tuần này", v.v.
    """
    logger.info("Tool get_current_datetime called")
    now = datetime.now()
    return json.dumps({
        "success": True,
        "current_datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "current_day_of_week": now.strftime("%A")
    }, ensure_ascii=False)

@tool
def calculate_date_of_weekday(weekday: str, relative_week: str = "this_week") -> str:
    """
    Tính toán ngày tháng chính xác cho một thứ trong tuần.
    Args:
        weekday: Thứ trong tuần (ví dụ: 'thứ 2', 'thứ 3', 'thứ 4', 'thứ 5', 'thứ 6', 'thứ 7', 'chủ nhật')
        relative_week: Tuần tương đối, có thể là 'last_week' (tuần trước), 'this_week' (tuần này), 'next_week' (tuần sau). Mặc định là 'this_week'.
    """
    logger.info(f"Tool calculate_date_of_weekday called: {weekday}, {relative_week}")
    try:
        now = datetime.now()
        current_weekday = now.weekday() # 0 = Monday, 6 = Sunday
        
        # Parse target weekday
        weekday_lower = weekday.lower()
        if "2" in weekday_lower or "hai" in weekday_lower: target_weekday = 0
        elif "3" in weekday_lower or "ba" in weekday_lower: target_weekday = 1
        elif "4" in weekday_lower or "tư" in weekday_lower: target_weekday = 2
        elif "5" in weekday_lower or "năm" in weekday_lower: target_weekday = 3
        elif "6" in weekday_lower or "sáu" in weekday_lower: target_weekday = 4
        elif "7" in weekday_lower or "bảy" in weekday_lower: target_weekday = 5
        elif "chủ nhật" in weekday_lower or "chu nhat" in weekday_lower: target_weekday = 6
        else:
            return json.dumps({"success": False, "error": f"Không nhận diện được thứ '{weekday}'."}, ensure_ascii=False)
            
        # Calculate days difference from today to the target weekday of THIS week
        days_diff = target_weekday - current_weekday
        target_date = now + timedelta(days=days_diff)
        
        # Adjust based on relative_week
        if relative_week == "last_week":
            target_date -= timedelta(weeks=1)
        elif relative_week == "next_week":
            target_date += timedelta(weeks=1)
            
        return json.dumps({
            "success": True,
            "query": f"{weekday} {relative_week}",
            "calculated_date": target_date.strftime("%Y-%m-%d"),
            "formatted_date": target_date.strftime("%d/%m/%Y")
        }, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Error in calculate_date_of_weekday: {e}")
        return json.dumps({"success": False, "error": str(e)}, ensure_ascii=False)

tools_list = [search_flights, search_hotels, calculate_budget, search_restaurants, search_attractions, get_current_datetime, calculate_date_of_weekday]
