from flask import Blueprint, request, jsonify
import logging

from controllers.project_controller import ProjectController  #  Business logic handler


from decorators.auth import login_required
#  Define the blueprint for RESTful API endpoints
api_project_routes = Blueprint("api_project_routes", __name__)
controller = ProjectController()
logger = logging.getLogger(__name__)
from middleware.api_key_required import require_api_key

# ===========================
#  GET all projects
# ===========================
@api_project_routes.route("/api/projects", methods=["GET"])
@require_api_key
def get_all_projects():
    try:
        
        #  Retrieve all project objects using the controller
        projects = controller.get_all_projects()

        # Return Custom response to the client if no project founds with explaining message 
        if not projects : 
            return jsonify({ "status" : "success" , "message" : "No Projects Found.", "data" : [] }) , 200 
        # after beign sure that at list there one project retrieved we convert project objects to dictionaries for JSON serialization
        project_list = [project.to_dict() for project in projects]

         

        # Return success response with project data
        return jsonify({"status": "success", "data": project_list}), 200
    except Exception as e:

        
        # Log the error with full stack trace (optional but useful in debugging)
        logger.exception("GET /api/projects failed")  # Better than logger.error for traceback


        # return a generic error message to the client
        return jsonify({"status": "error", "message": "Could not retrieve projects"}), 500

# ===========================
# GET a single project by ID
# ===========================

@api_project_routes.route("/api/projects/<int:project_id>", methods=["GET"])
@require_api_key
def get_project_by_id(project_id):
    try:
        project = controller.get_project_by_id(project_id)
        if project:
            return jsonify({"status": "success", "data": project.to_dict()}), 200
        else:
            return jsonify({"status": "error", "message": "Project not found"}), 404
    except Exception as e:
        logger.error(f"GET /api/projects/{project_id} failed: {e}")
        return jsonify({"status": "error", "message": "Could not retrieve project"}), 500

# ===========================
# ✅ POST create a new project
# ===========================

@api_project_routes.route("/api/projects", methods=["POST"])
@login_required 
@require_api_key
def create_project():
    try:
        data = request.get_json()
        if controller.create_project(data):
            return jsonify({"status": "success", "message": "Project created"}), 201
        else:
            return jsonify({"status": "error", "message": "Project creation failed"}), 400
    except Exception as e:
        logger.error(f"POST /api/projects failed: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# ===========================
# ✅ PUT update existing project
# ===========================
@api_project_routes.route("/api/projects/<int:project_id>", methods=["PUT"])
@login_required
@require_api_key
def update_project(project_id):
    try:
        data = request.get_json()
        if controller.update_project(project_id, data):
            return jsonify({"status": "success", "message": "Project updated"}), 200
        else:
            return jsonify({"status": "error", "message": "Project not found or update failed"}), 404
    except Exception as e:
        logger.error(f"PUT /api/projects/{project_id} failed: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500

# ===========================
# ✅ DELETE a project
# ===========================
@api_project_routes.route("/api/projects/<int:project_id>", methods=["DELETE"])
@login_required
@require_api_key
def delete_project(project_id):
    try:
        if controller.delete_project(project_id):
            return jsonify({"status": "success", "message": "Project deleted"}), 200
        else:
            return jsonify({"status": "error", "message": "Project not found or deletion failed"}), 404
    except Exception as e:
        logger.error(f"DELETE /api/projects/{project_id} failed: {e}")
        return jsonify({"status": "error", "message": "Internal server error"}), 500
