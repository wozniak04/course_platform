from flask import Flask, request, jsonify
from src.schoolmanager import SchoolManager
from src.user import User
from src.course import Course

app = Flask(__name__)
manager = SchoolManager()

@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    user = User(data['email'], data['age'], data.get('region', 'PL'))
    if user.email == "invalid":
        return jsonify({"message": "zły email lub wiek"}), 400
    if manager.get_user_by_email(user.email) is not None:
        return jsonify({"message":"email already registered"}),409
    manager.register_user(user)
    return jsonify({"email": user.email, "status": "registered"}), 201

@app.route('/users', methods=['GET'])
def get_users():
    return jsonify([{"email": u.email, "region": u.region} for u in manager.users]), 200

@app.route('/users/<email>', methods=['GET'])
def get_user_by_email(email):
    user = manager.get_user_by_email(email)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "email": user.email, 
        "age": user.age, 
        "region": user.region, 
        "is_premium": user.is_premium,
        "courses": user.saved_courses
    }), 200

@app.route('/users/count', methods=['GET'])
def get_users_count():
    return jsonify({"count": manager.number_of_users()}), 200

@app.route('/users/<email>', methods=['DELETE'])
def delete_user(email):
    if manager.delete_user(email):
        return jsonify({"message": f"User {email} deleted"}), 200
    return jsonify({"error": "User not found"}), 404


@app.route('/courses', methods=['POST'])
def add_course():
    data = request.get_json()
    course = Course(data['title'], data['price'], data['materials_count'], data['owner'])
    if manager.get_course_by_title(course.title) is not None:
        return jsonify({"message": "course with this title already exists"}),409
    if data.get('published', False):
        course.publishCourse()
    manager.add_course(course)
    return jsonify({"title": course.title, "status": "added"}), 201

@app.route('/courses', methods=['GET'])
def get_courses():
    return jsonify([
        {"title": c.title, "price": c.price, "published": c.is_published, "owner": c.owner} 
        for c in manager.courses
    ]), 200

@app.route('/courses/<title>', methods=['GET'])
def get_course_by_title(title):
    course = manager.get_course_by_title(title)
    if not course:
        return jsonify({"error": "Course not found"}), 404
    return jsonify({
        "title": course.title,
        "price": course.price,
        "owner": course.owner,
        "published": course.is_published,
        "reviews": course.reviews
    }), 200

@app.route('/courses/<title>', methods=['PATCH'])
def update_course(title):
    course = manager.get_course_by_title(title)
    if not course:
        return jsonify({"error": "Course not found"}), 404

    data = request.get_json()
    new_title = data.get('title')
    
    if new_title and new_title != title:
        if manager.get_course_by_title(new_title):
            return jsonify({"message": "course with this title already exists"}), 409

    course.update_data(
        title=new_title,
        price=data.get('price'),
        materials_count=data.get('materials_count')
    )
    
    return jsonify({"message": "Course updated", "title": course.title}), 200

@app.route('/courses/count', methods=['GET'])
def get_courses_count():
    return jsonify({"count": manager.number_of_courses()}), 200

@app.route('/courses/<title>', methods=['DELETE'])
def delete_course(title):
    if manager.delete_course(title):
        return jsonify({"message": f"Course {title} deleted"}), 200
    return jsonify({"error": "Course not found"}), 404

@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.get_json()
    user = manager.get_user_by_email(data['email'])
    course = manager.get_course_by_title(data['title'])
    
    if not user or not course:
        return jsonify({"error": "User or Course not found"}), 404
    
    result = manager.enroll(user, course)
    if result is True:
        return jsonify({"status": "success"}), 200
    return jsonify({"error": result}), 400

@app.route('/review', methods=['POST'])
def add_review():
    data = request.get_json()
    user = manager.get_user_by_email(data['email'])
    
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    result = manager.add_review(user, data['title'], data['rating'], data['comment'])
    if isinstance(result, str):
        return jsonify({"error": result}), 400
    return jsonify(result), 201

@app.route('/price', methods=['POST'])
def get_calculated_price():
    data = request.get_json()
    user = manager.get_user_by_email(data['email'])
    course = manager.get_course_by_title(data['title'])
    
    if not user or not course:
        return jsonify({"error": "User or Course not found"}), 404
        
    final_price = manager.calculate_price(course, user)
    return jsonify({"final_price": final_price}), 200



@app.route('/clear', methods=['DELETE'])
def clear_data():
    manager.users = []
    manager.courses = []
    return jsonify({"message": "Data cleared"}), 200