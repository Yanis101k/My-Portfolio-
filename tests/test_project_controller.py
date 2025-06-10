import unittest 
import sqlite3 # Built-in Python module to interact with SQLite databases

# the sys module allow us to interact with the Python interpreter . it's useful for handling system-specific information
#and controlling the program's behavior 
#Add path for module search 
import sys 

# the os module in python gives you access to operating system features like : 
# reading or writing files , navigating folders , and managing environment variables.
# Used to set environment variables during testing 

import os 

#  Make root directory visible to python se we can import config.py
sys.path.append( os.path.abspath( os.path.join( os.path.dirname(__file__) , '..' )))

# Set environment variable to use a temporary database
os.environ["DATABASE_PATH"] = "database/test_portfolio.db"

from database.connector import DatabaseConnector # Manages SQLite connection
from database.project_dao import ProjectDAO # class that interact with the databse directly using sql 
from models.project import Project # project model for output and input 
from controllers.project_controller import ProjectController # class to test 

class TestProjectController( unittest.TestCase ) :
    """
     Unit test class for ProjectController
     uses a temporary database file to test full CRUD functionalities 
    """ 
    def setUp(self) :
        """
            This run before each test. It creates : 
            - a fresh test DB
            - a DB connection 
            - tables using schema.sql
            - ProjectController instance 
        """

        # Create and connect to test database
        self.db = DatabaseConnector()
        self.conn = self.db.connect() 

        # Load schema to create tables 
        with open("database/schema.sql" , "r" ) as f : 
            self.conn.executescript(f.read())
        
        # create an instance of project controller 
        self.project_controller = ProjectController()

    def tearDown(self):
        """
           Runs after each test to close DB and delet test databse file 
        """  
        self.db.close()

        if os.path.exists("database/test_portfolio.db") :
            os.remove("database/test_portfolio.db")

    
    def test_get_and_add_project( self ) : 
         """
            test approach :
             step 1 : get projects from our empty database 
                      and be sure that the returned list is empty
            
             step 2 : create 2 project and try to retrieve them 
                      and be sure that the length of returned list is 2 
                      and contain the prjects that we inserted before 
         """

         projects = self.project_controller.get_all_projects() 

         self.assertEqual(len(projects) , 0 )

         # define a list of projects dictionaries with 2 projects 
         projects_dicts_to_create = [
                         { "id" : None , "title" : "project title 1" , "description" : "project description 1" , "image_url" : None , "github_url" : None , "live_url" : None } , 
                         { "id" : None , "title" : "project title 2" , "description" : "project description 2" , "image_url" : None , "github_url" : None , "live_url" : None }                  
                        ] 
         
         # create two projects 
         self.project_controller.create_project( projects_dicts_to_create[0] )
         self.project_controller.create_project( projects_dicts_to_create[1] )
         
         projects_list_retrived_after_creation = self.project_controller.get_all_projects()
         self.assertEqual( len( projects_list_retrived_after_creation ) , 2 )

         # convert the " projects_list_retrived_after_creation " to dictionary
         projects_dicts_retrived_after_creation = [
                                                    { "id" : None , "title" : projects_list_retrived_after_creation[0].get_title() , "description" : projects_list_retrived_after_creation[0].get_description() , "image_url" : None , "github_url" : None , "live_url" : None } , 
                                                    { "id" : None , "title" : projects_list_retrived_after_creation[1].get_title() , "description" : projects_list_retrived_after_creation[1].get_description() , "image_url" : None , "github_url" : None , "live_url" : None } 
                                                    ]
         self.assertEqual( projects_dicts_retrived_after_creation  , projects_dicts_to_create )

    def test_get_project_by_id( self ) : 
        """
            test approach :
             step 1 : get project by an id from our empty database 
                      and be sure that the return value is None
            
             step 2 : create 3 projects and try to retrieve them one by one  
                      and be sure that it return the correct one 
             
             step 3 : try to retrive a project that doesn't exist 
                      and be sure that it return None value
         """
        project_id_to_filter_with = 3 ; 
        project = self.project_controller.get_project_by_id( project_id_to_filter_with )
        self.assertIsNone( project )

        # define a list of projects dictionaries with 2 projects 
        projects_dicts_to_create = [
                         { "id" : None , "title" : "project title 1" , "description" : "project description 1" , "image_url" : None , "github_url" : None , "live_url" : None } , 
                         { "id" : None , "title" : "project title 2" , "description" : "project description 2" , "image_url" : None , "github_url" : None , "live_url" : None } ,                   
                         { "id" : None , "title" : "project title 3" , "description" : "project description 3" , "image_url" : None , "github_url" : None , "live_url" : None }
                        ] 
        # create three projects 
        self.project_controller.create_project( projects_dicts_to_create[0]  )
        self.project_controller.create_project( projects_dicts_to_create[1]  ) 
        self.project_controller.create_project( projects_dicts_to_create[2]  )  
        
        # now we have three projects in our database with those id's ( 1 , 2 , 3 )   
        # filter the first project that have it id 1 
        project_id_to_filter_with = 1 
        filtred_project = self.project_controller.get_project_by_id( 1 )
        filtred_project_dict  = { "id" : None  , "title" : filtred_project.get_title() , "description" : filtred_project.get_description() ,
                                  "image_url" : None , "github_url" : None , "live_url" : None }
        self.assertEqual( filtred_project_dict , projects_dicts_to_create[0] )

        # filter the first project that have it id 2
        project_id_to_filter_with = 2
        filtred_project = self.project_controller.get_project_by_id( 2 )
        filtred_project_dict  = { "id" : None  , "title" : filtred_project.get_title() , "description" : filtred_project.get_description() ,
                                  "image_url" : None , "github_url" : None , "live_url" : None }
        self.assertEqual( filtred_project_dict , projects_dicts_to_create[1] )


        # filter the first project that have it id 3
        project_id_to_filter_with = 3
        filtred_project = self.project_controller.get_project_by_id( 3 )
        filtred_project_dict  = { "id" : None  , "title" : filtred_project.get_title() , "description" : filtred_project.get_description() ,
                                  "image_url" : None , "github_url" : None , "live_url" : None }
        self.assertEqual( filtred_project_dict , projects_dicts_to_create[2] )
        
        # try to retrive a project that doesn't exist 
        project_id_to_filter_with = 4
        filtred_project = self.project_controller.get_project_by_id( 4 )
        self.assertIsNone( filtred_project )                                
    
    def test_update_project( self ) :
        """
          test approach : 

             step 1 : try to update a project that doesn't exist and be sure that nothing is updated 
             step 2 : try to update a project that exist and be sur that is updated 
        """ 

        # create three projects 

        projects_dicts_before_updating  = [
                         { "id" : None , "title" : "project title 1" , "description" : "project description 1" , 
                          "image_url" : None , "github_url" : None , "live_url" : None } , 

                         { "id" : None , "title" : "project title 2" , "description" : "project description 2" , 
                           "image_url" : None , "github_url" : None , "live_url" : None } ,          

                         { "id" : None , "title" : "project title 3" , "description" : "project description 3" , 
                          "image_url" : None , "github_url" : None , "live_url" : None }
                        ]
        
        self.project_controller.create_project(projects_dicts_before_updating [0] )
        self.project_controller.create_project(projects_dicts_before_updating [1] )
        self.project_controller.create_project(projects_dicts_before_updating [2] )

        # try to update a project that doesn't exist 
        project_id_to_update = 4
        project_to_update_with =  { "id" : None , "title" : "project to update with title 2" , 
                                   "description" : "project to update with description 2" , 
                                   "image_url" : None , "github_url" : None , "live_url" : None } 
        self.project_controller.update_project( project_id_to_update , project_to_update_with )

        # be sure that any of our projects doesn't updated 
    
    
        projects_list_after_updating = self.project_controller.get_all_projects() 
        project_dicts_after_updating = [
                         { "id" : None , "title" : projects_list_after_updating[0].get_title() , 
                          "description" : projects_list_after_updating[0].get_description() , 
                          "image_url" : projects_list_after_updating[0].get_image_url() , 
                          "github_url" : projects_list_after_updating[0].get_github_url() , 
                          "live_url" : projects_list_after_updating[0].get_live_url() } , 
                           
                           { "id" : None , "title" : projects_list_after_updating[1].get_title() , 
                            "description" : projects_list_after_updating[1].get_description() , 
                          "image_url" : projects_list_after_updating[1].get_image_url() , 
                          "github_url" : projects_list_after_updating[1].get_github_url() , 
                          "live_url" : projects_list_after_updating[1].get_live_url() } , 

                          { "id" : None , "title" : projects_list_after_updating[2].get_title() , 
                           "description" : projects_list_after_updating[2].get_description() , 
                          "image_url" : projects_list_after_updating[2].get_image_url() , 
                          "github_url" : projects_list_after_updating[2].get_github_url() , 
                          "live_url" : projects_list_after_updating[2].get_live_url() } 
                        ]  
        
        self.assertEqual( project_dicts_after_updating , projects_dicts_before_updating )
        
        # try to update an existing project and be sur that's updated 
        project_id_to_update = 2 
        self.project_controller.update_project( project_id_to_update , project_to_update_with )
        projects_list_after_updating = self.project_controller.get_all_projects()

        # the resulted projects dicts after deleting 
        project_dicts_after_updating = [
                         { "id" : None , "title" : projects_list_after_updating[0].get_title() , 
                          "description" : projects_list_after_updating[0].get_description() , 
                          "image_url" : projects_list_after_updating[0].get_image_url() , 
                          "github_url" : projects_list_after_updating[0].get_github_url() , 
                          "live_url" : projects_list_after_updating[0].get_live_url() } , 
                           
                           { "id" : None , "title" : projects_list_after_updating[1].get_title() , 
                            "description" : projects_list_after_updating[1].get_description() , 
                          "image_url" : projects_list_after_updating[1].get_image_url() , 
                          "github_url" : projects_list_after_updating[1].get_github_url() , 
                          "live_url" : projects_list_after_updating[1].get_live_url() } , 

                          { "id" : None , "title" : projects_list_after_updating[2].get_title() , 
                           "description" : projects_list_after_updating[2].get_description() , 
                          "image_url" : projects_list_after_updating[2].get_image_url() , 
                          "github_url" : projects_list_after_updating[2].get_github_url() , 
                          "live_url" : projects_list_after_updating[2].get_live_url() } 
                        ]  
        # the expected projects dicts after updating 
        expected_projects_dicts_after_updating = [
                                                    { "id" : None , "title" : "project title 1" , "description" : "project description 1" , 
                                                     "image_url" : None , "github_url" : None , "live_url" : None } ,
                                                    
                                                    project_to_update_with , 

                                                    { "id" : None , "title" : "project title 3" , "description" : "project description 3" , 
                                                     "image_url" : None , "github_url" : None , "live_url" : None }
                                                 ]
        
        self.assertEqual( project_dicts_after_updating , expected_projects_dicts_after_updating )

    def test_delete_project( self ) : 
        """
           test approach : 
                step 1 : try to delete a project that doesn't exist 
                         and be sure that nothing is happend 
                
                step 2 : try to delet a project that exist 
                         and be sur that is deleted correctly
                
        """                          

        projects_dicts_before_deleting = [
                                      { "id" : None , "title" : "project title 1" , "description" : "project description 1" , 
                                        "image_url" : None , "github_url" : None , "live_url" : None } , 

                                      { "id" : None , "title" : "project title 2" , "description" : "project description 2" , 
                                        "image_url" : None , "github_url" : None , "live_url" : None } ,          

                                      { "id" : None , "title" : "project title 3" , "description" : "project description 3" , 
                                        "image_url" : None , "github_url" : None , "live_url" : None }
                                   ]
        
        # create three projects 
        self.project_controller.create_project( projects_dicts_before_deleting[0] )
        self.project_controller.create_project( projects_dicts_before_deleting[1])
        self.project_controller.create_project( projects_dicts_before_deleting[2])

        # at this point we have three projects in our database with ( 1 , 2 , 3 ) as ID's 
        # let's try to delet a project that doesn't exist 
        project_id_to_delete = -1 
        self.project_controller.delete_project( project_id_to_delete)

        projects_list_after_deleting = self.project_controller.get_all_projects()
        
        project_dicts_after_deleteing = [
                         { "id" : None , "title" : projects_list_after_deleting[0].get_title() , 
                          "description" : projects_list_after_deleting[0].get_description() , 
                          "image_url" : projects_list_after_deleting[0].get_image_url() , 
                          "github_url" : projects_list_after_deleting[0].get_github_url() , 
                          "live_url" : projects_list_after_deleting[0].get_live_url() } , 
                           
                           { "id" : None , "title" : projects_list_after_deleting[1].get_title() , 
                            "description" : projects_list_after_deleting[1].get_description() , 
                          "image_url" : projects_list_after_deleting[1].get_image_url() , 
                          "github_url" : projects_list_after_deleting[1].get_github_url() , 
                          "live_url" : projects_list_after_deleting[1].get_live_url() } , 

                          { "id" : None , "title" : projects_list_after_deleting[2].get_title() , 
                           "description" : projects_list_after_deleting[2].get_description() , 
                          "image_url" : projects_list_after_deleting[2].get_image_url() , 
                          "github_url" : projects_list_after_deleting[2].get_github_url() , 
                          "live_url" : projects_list_after_deleting[2].get_live_url() } 
                                       ]
        self.assertEqual( projects_dicts_before_deleting , project_dicts_after_deleteing )

        # Now let's try to delet a project that exist 
        project_id_to_delete = 2 
        self.project_controller.delete_project( 2 )
        projects_list_after_deleting = self.project_controller.get_all_projects()
        self.assertEqual( len( projects_list_after_deleting ) , 2 )
        # resulted projects dicts after deleting  
        project_dicts_after_deleteing = [
                         { "id" : None , "title" : projects_list_after_deleting[0].get_title() , 
                          "description" : projects_list_after_deleting[0].get_description() , 
                          "image_url" : projects_list_after_deleting[0].get_image_url() , 
                          "github_url" : projects_list_after_deleting[0].get_github_url() , 
                          "live_url" : projects_list_after_deleting[0].get_live_url() } , 
                           
                           { "id" : None , "title" : projects_list_after_deleting[1].get_title() , 
                            "description" : projects_list_after_deleting[1].get_description() , 
                          "image_url" : projects_list_after_deleting[1].get_image_url() , 
                          "github_url" : projects_list_after_deleting[1].get_github_url() , 
                          "live_url" : projects_list_after_deleting[1].get_live_url() } ]
        
        # projects dicts expected ( the correct one ) after deleting 
        expected_projects_dicts_after_deleting = [
                                                   { "id" : None , "title" : "project title 1" , "description" : "project description 1" , 
                                                      "image_url" : None , "github_url" : None , "live_url" : None } , 
                                                    { "id" : None , "title" : "project title 3" , "description" : "project description 3" , 
                                                      "image_url" : None , "github_url" : None , "live_url" : None }
                                                 ]
        
        self.assertEqual( project_dicts_after_deleteing , expected_projects_dicts_after_deleting )

if __name__ == '__main__':

    unittest.main()