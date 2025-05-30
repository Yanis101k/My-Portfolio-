
# ========================
# Project Model 
# Represents one portfolio project from database 
#==========================

# Define a Project class to represent a project record 

class Project : 

    def __init__( self , id , title , description , image_url=None 
                 , github_url=None , live_url=None , created_at=None ): 
        
        """
        Constructor to initialize a project instance.

        :param id: Unique identifier for the project (from the database)
        :param title: Title of the project
        :param description: Description of the project
        :param image_url: Optional image path or URL
        :param github_url: Optional GitHub repository link
        :param live_url: Optional live preview link
        :param created_at: Optional timestamp of creation

        """
        
        self.__id = id  # Private Attribute Unique project ID (integer)
        self.__title = title # Private Attribute Project title (string)
        self.__description = description # Private Attribute Detailed description (string)
        self.__image_url = image_url # Private Attribute Path or URL to image (string or None)
        self.__github_url = github_url # Private Attribute GitHub repo link (string or None)
        self.__live_url = live_url # Private Attribute Live preview URL (string or None)
        self.__created_at = created_at # Private Attribute Timestamp from database (string or None)
    

    # ===================
    # Getters
    # ===================

    def get_id(self):
        return self.__id

    def get_title(self):
        return self.__title

    def get_description(self):
        return self.__description

    def get_image_url(self):
        return self.__image_url

    def get_github_url(self):
        return self.__github_url

    def get_live_url(self):
        return self.__live_url

    def get_created_at(self):
        return self.__created_at

    # ===================
    # Setters
    # ===================

    def set_title(self, title):
        self.__title = title

    def set_description(self, description):
        self.__description = description

    def set_image_url(self, image_url):
        self.__image_url = image_url

    def set_github_url(self, github_url):
        self.__github_url = github_url

    def set_live_url(self, live_url):
        self.__live_url = live_url

    # ===================
    # Utility Methods
    # ===================

    def to_dict(self):
        """
        Convert the Project object to a dictionary.
        Useful for returning JSON or rendering templates.
        """
        return {
            "id": self.__id,
            "title": self.__title,
            "description": self.__description,
            "image_url": self.__image_url,
            "github_url": self.__github_url,
            "live_url": self.__live_url,
            "created_at": self.__created_at
        }

    def __repr__(self):
        """
        Developer-friendly string representation.
        """
        return f"<Project {self.__id}: {self.__title}>"