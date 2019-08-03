import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_1(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Git Path", "Path", """Changes the git working directory from the current location""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("504cb3de-8ebc-42d7-a745-4554f35f0cb4")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "path", "path", "The working directory path to be used by git")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "create_path", "create_path", "Determines whether the given path will be created (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "set", "set", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIESURBVEhLrZVLqE1RHIePROT9GsijPMLAwCMMTJQMRMrAxEjI9E6UcG8uA6KYIQxEMmPAiJkBEqIwMJDbLdQVA+/cXL7vv85u3845d+9znPPVV+u39jlrr7X2elSaZApuwW48g4dxM07CthiPJ/AX/sXf+BkHq/kHHsWx2DKL8DXa0FlcjRNwFE7EtXgBff4C52HTzMIPVVdYUcAa/IR9ONWKZriDP7G2V45iG66MlLMY/+DNSCWsR4e9M1JiCT5G6zMf4ALM2IfW24lCruPHVAym43t0urajL9uBTstbnIwyGr/gxUgF2NiVVAyOoT2bHynHF1l/IFLCKXqTio1xWboED0ZKPMF7qVhH7bPj+B0dTUPGoWu9J1LCuX6UinW8xLupGJzErzjiC8R5vZGKQRc6Fesi5WxA6/dGSrj6XqXiyJxDh5ntTkflVNiYR8VW7K3m+zgGxU3o6E9FKmA5+uf9kRJuoGtofeZlHH4WHUHr3ROlXMUhnB0pZyYuwxmRcuaijZcu0Yxp6EF2O1I5/s5pzfZEU+xCe+UxXcQm9He7I7XIQxxAP3QjXI79+CzSf7AU7d3pSPUcQp/XHn4t4e60EVfXcOag9ZcitYHr/B0+jZRzC10IXqdtk31Ij2TZiOY9kTqEx4cH4UL0xHyOHcVr9Bt6L9j7VdhxslvrfKRSKpV/IC50TXykfQYAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, path, create_path, set):
        
        report = None
        help = None
        
        if set and path:
            if (not os.path.exists(path)) and create_path:
                os.mkdir(path)
            os.chdir(path)
            rsc.sticky["git_path"] = os.getcwd()
        
        help = "Press the set button To set the git path\n"
        if not path: help+= "\n * You need to first enter a path\n"
        if not create_path : help += "\n* If the path doeasn't exist, you can use the create_path option"
        
        
        report = "The current working directory is:\n" + str(os.getcwd())
        
        return (report, help)

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc

class Githopper_2(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Create Git Repository", "Create Git", """Initializes the git repository (git init equivalent)""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("fae82167-2de3-4054-9be4-c10a5509d306")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_name", "user_name", "The username used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_email", "user_email", "The email used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "initialize", "initialize", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGdSURBVEhLzdXNK0RRGMfxm9ciRTZey1tYKH8AshKxsvUfWChZKsrWwsqKKAsLa6/lpVCKjbKwtRIRC5LyEt/fOffkds3NTGem/OqT81zT85w5M/dO8J/ShXy7zG7ysI0vHKIYWYt2vI5bDOMBJ8jKEDXfhXY+ogukGo/wHqLme7jHKu4whSo0wmuImu/jBS26QC6hd7JhKo8h0ebtuhBmDBrwiW5dIBkPSWqu1OEZp9CgHig1SGtICTahb0m8udKKdzRjAa9YQy0acIMDlCFleqGdDZjqdzRA/9df5Q2qZ01lj031oKlSRJO1g2vobONxAzpNFQQT2EITdExX0DGVIzE6Q71IZxofUg8NaDPVTyqh4zlHqS78laQh49CASVPZaOcZNXdJNWQHGnBsKo/mLvEh+rZMh2vv5i7RIXoGKRVIar6CGbtMP26I7o9+6FuWtHO9btkuM4uG6HdAn8EZos2LoFqOsBSpC5F2CtAHDYtmDk+hD+gGdPUovNOBodAF9Mvn6vi95B09KOftMjfRZ7Bol7mJnrR6rEcSBN/Rl2f8RlX+tgAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, user_name, user_email, initialize):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            """
            
            try:
                out_put = Popen(["cmd", "/C"] + cmd)
            except:
                pass
        
        def executor_alt(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def init(user_name, user_email):
            
            if user_name:
                executor_alt(["git", "config", "--global", "user.name", user_name])
            if user_email:
                executor_alt(["git", "config", "--global", "user.email", user_email])
            
            cwd = os.getcwd().split("\\")
            if cwd.pop() != "System":
                executor(["git", "init"])
            else:
                return ("Error: The repository could not be created\n"
                        "\n* Please use the \"Git Path\" component to specify the path "
                        "for your local git repository")
                
            if os.path.exists(".git"):
                init_msg = "The git repository initialized successfully"
            else:
                return ("Error: The repository could not be created\n"
                    "\n* Please make sure you have done the following:\n"
                    "1 - Install the Git software from www.git-scm.com\n"
                    "2 - Set Rhino to Run as Administrator if you are using the C drive")
            
            return init_msg
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if initialize:
            r = init(user_name, user_email)
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the initialize button to create the new repository\n"
        if not user_name: help +="\n* You need to enter a user_name first\n"
        if not user_email: help += "\n* You need to enter a user_email first\n"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_2"]
        except:
            rsc.sticky["Githopper_2"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_2"] == None:
            rsc.sticky["Githopper_2"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_2"]
            rsc.sticky["Githopper_2"] = None
        
        return (report, help)

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc

class Githopper_3(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Clone Repository", "Clone", """Clones a remote git repository (makes a local copy)""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("2350aed6-c8b1-42f3-bc14-3112e961848c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "URL", "URL", "Address of the remote git repository (GitHub link)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "location", "location", "Location that is used to store the cloned git repository")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_name", "user_name", "The username used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "user_email", "user_email", "The email used to sign git commits by Githopper")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "clone", "clone", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        p4 = self.marshal.GetInput(DA, 4)
        result = self.RunScript(p0, p1, p2, p3, p4)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIESURBVEhLxZVBSFRRFED/wkAsUoQKsmVFgbhKQqKFiZsEFxaZEbkKKhAsLGgRBILUtpViULhwlUEQVJuwNkqEuIjKRdYqKKVFuChC65w3Pmaa/2eacqADh/n3zZ9733/3vzfJ/+A4juM9vImtWBXq8Rn+zPA6RjbhfjyKR3AHRmrWPzOZxgW8hk/QJ3iIl9EiZ1Ga8Sq+Rse/4hW8hCcwk8PozS5NFib5jLUhymPxHxifNE4ihUvgDV0hSnMH/b4lRL8zhbHAkANZ2ExvaA9RmlH0+4MhynMIZ/ANvseLmMlpXMUHaLML2Ycuz3fc5kAJbL5m0oivcBKfoo2UAVxBZz/mQAE78RGeD1EFdONzHMHtDsAwmvwFbnVgHZMv4iz65L5FFdGGLtPuECXJGbyFm0OUowmX0aJiH5xExUXKsQs/4ku0qRfQnnXihouY3JnfD1GS3ECTuvtlQ0WKk8te/IImtX/SgX9dJCt5ZA4fo0l7HADPJ2N3+R/xvf+AEyFKYx/cnO4jk9qbLejR8w3PYVn2oD/sC1EaCxzLXSaf0HtdOnFz3s5dlifOzs9i3mEs4I4/gHXo0WHzva4I90NxkQZcwsEQ5XmLbsCSx0Yp+rGwSIz9DxHX/p+TR+KTnEQf/y76J1OV5JE4894Q5aha8kgs4kk6j1VNHjmFa+jxXiJ5kvwCY+uA63XPUxoAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, URL, location, user_name, user_email, clone):
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            """
            
            try:
                Popen(["cmd", "/C"] + cmd)
            except:
                pass
        
        def executor_alt(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def clone_repository(repository_address, user_name, user_email):
            """
            Clones the remote repository from it's address
            """
            
            a = executor_alt(["git", "config", "--global", "user.name"])
            b = executor_alt(["git", "config", "--global", "user.email"])
            
            if user_name and user_email:
                creds = ["git", "config", "--global","user.name", user_name]
                creds += ["&", "git", "config", "--global", "user.email", user_email]
                executor_alt(creds)
            
            if a and b:
                executor(["git", "clone", str(repository_address)])
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        if clone and URL and location:
            if not os.path.exists(location): os.mkdir(location)
            real_location = os.getcwd()
            os.chdir(location)
            clone_repository(URL, user_name, user_email)
            os.chdir(real_location)
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the clone button to clone the remote repository\n"
        
        if not URL:
            help += ("\n* Please enter the git url."
                      "\n  For example:"
                      "\n  https://github.com/account/Project\n")
        
        if not location:
            help += ("\n* Please enter the location."
                      "\n  For example:"
                      "\n  C:\\Projects\n")
        
        if not (executor_alt(["git", "config", "--global", "user.name"]) and executor_alt(["git", "config", "--global", "user.email"])):
            help += ("\n* You must enter a user_name and user_email for the first time")
        
        return help

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc

class Githopper_4(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Set Remote Address", "Remote", """Sets/Changes the address of remote repository for git""", "Githopper", "Beginning")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("3dda517f-a117-42e2-8bf0-a4b2d6a53925")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "URL", "URL", "Address of the remote git repository (GitHub link)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "replace", "replace", "Determines whether an existing remote address could be replaced")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "set", "set", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFySURBVEhL7dW/K0VhHMfxk+GSgSgZDAYMbAzCzIRFKWWwCJNNKUYGJf8CiZj8GE12MwOrKL/y22DA+1PnW0+355zzHO6k+6lX5z7f+3yf7u1+z7lROaVOLRrja8nSgiWc4A6v8VXrZbTi11nAO75TfGARubMN34FJdhCcVajpCpt4iNfFVN/AdbxeQ2a6YQesq0CaMIkB6H1dtVZd0T7r6VEhLXuwzYcqBGQf1nOgQlLq8ALbPI2QTMF6NGX18KYXtvEWVQhJJW5gvX3wZhC26UKFHDmH9Q6p4Es/bNMTQu/YGjzCejUE3uiu/IJtHENIRmE96m+DNxU4hTZ+4g1ZY6f37T6QM+icxMxCG+ewFb8+wgTcjENj7H5jUX9qCtCneEYzdqHRm4GbebgHi/o0UZlphx5ix9DjuQHF0aS4h+tH7kBwOqFnkZo148NwMwI7XCPdhdzR+K3gHjrQje6ZS+g/4c9/QNXQb+NGa9X/daLoB/OXg/hnM6GqAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, URL, replace, set):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def change_origin(url, r=False):
            co_msg = executor(["git", "remote", "add", "origin", url])
            
            if r : co_msg = executor(["git", "remote", "set-url", "origin", url])
            
            return co_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if str(URL).endswith(".git") and str(URL).startswith("https:") and set:
            change_origin(URL, replace)
            r = "The remote address is as follows:\n" + executor(["git", "remote", "-v"])
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the set button to set the remote repository address\n"
        
        if not URL:
            help += ("\n* Please enter the git url."
                      "\n  For example:"
                      "\n  https://github.com/account/Project\n")
        
        if not replace:
            help += "\n* If you want to allow git to overwrite old remote addresses, set replace toggle to True\n"
        else:
            help += "\n* The old remote addresses will be overwriten\n"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_4"]
        except:
            rsc.sticky["Githopper_4"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_4"] == None:
            rsc.sticky["Githopper_4"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_4"]
            rsc.sticky["Githopper_4"] = None
        
        return (report, help)

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_5(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Check Status", "Status", """Provides a status report of the local git repository""", "Githopper", "Status")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("8695d84d-4069-47e9-a2f2-e0b007ce460c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "check", "check", "Refreshes the status (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "status", "status", "Status report of the local git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHqSURBVEhL3dXLSxVhHIfxMexiWVq6LcouJFjQBVK7QLQoyFqVtU7EjaAQEhH9B7VJoV0g2AVpH0FXU7GLi+i6ChdR0LZFW59n3jOHOTfOdA606Asf5sd5z8w78877vhP9d2mq02qUTRte4hM+1uELrqAkR7GEndiBLX9pKzxvGK9REjt4G8o4m9AOn6wa/7cW5hh+YgKDWIE4R7AYyqgTH+Djfs7gK+7AnMB33MBv7EWcdAeVshKtoayYs3gayugNekNZ2MFm3Mb9FO/wOMxNPEC6/RpMH2ZCGV+vO5SFHZzHL4zmjOA57sGcw0CRUzBnULWDC3gcynzs6G4o43e0H/tyrLfDZOqgH89Cmc9VTIYymoZTcSHHehwm0xBdxJNQ5jMGx7paMj3BSfzBK8zmjj9wC+YhnCHeuVw/znuT6Qka0QWnWOIANsDsgvM7zZVsMj2Bq9OZ4UpM2wPjJBgqchomUwfejS90qkhyEVdp+ndnl5PAZBqieuJKfhHKwg7c7N6FsmQv8qhLMI/g/lNuL3KI3LZXwZffgziHYUOSFmyEe4+sG2DWobhtDUwz/K64sudwCHG8oN+Dy9iNbWX4rbCtI/VbwpVsW3K8jm9Yj3wOYh7pL1Qt3sP14xZSNo6f39Zaef6/ShQtA8+Ln7H2/gKRAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        status = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def stat():
            """
            reports the status of the local repository
            """
            
            status_msg = executor(["git", "status"])
            
            return status_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        status = stat()
        
        
        return status

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_6(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Branch Graph", "Graph", """Provides a text graph of commits including branches and merges""", "Githopper", "Status")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("79f504f6-2840-4e88-971c-159d9e8c360c")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = GhPython.Assemblies.MarshalParam()
        self.SetUpParam(p, "check", "check", "Refreshes the graph (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "graph", "graph", "Text graph of commits")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAG3SURBVEhLrdVNKARhHMfxUURSkqTk5eAikiKSg7xecXCguCiJIyWJUtxIHBwdcXByc1EKN5GIoigHDgp5fwvf38zO7tp27czu/OrTPs+08/xnn5dZI0ryfZ9OkodUqxk9SVjGOzaRjv8yjk+co1gXoqUaP2jGK1oQKWnQd/uwBz1Y1GTjEtvQzdOIlETsYB/36IWjlEGDT0FTpWmIlAzcYtHsOYzm/Qm5qIGKjUKFCxGaAwxZTWfRND2jyuwZRgO0kF94RCuCcwQ9gOPYBSrNnpUbjGAFmvPgeFJgAVe4w6AuBMV1AXsNSs1eIMdYtZp/cghXBSqghW0ze4Ho4IXbtmfQjnOUHFxjF9p+JbCzhXmr6U8/9DA6mI5SC93Q5PvsgZ3QAjrB+k6X2XOYFKxBN+pXZMKOCsxZTf/gnWbPZXQ631Bu9gLRGkygHRq8AzElC9qmWmw7jfiAzsMDYh5cCXcOLjCDdeiXxJVwBU6hN6cKzepCPLEL2Gugede0LEH7PRlxRX9/GrAAw9CC1sOzdEODbuAFdfAsRfjGJFRkAJ5GLzgNPAYV0on2PHrqE2hBE3TBfQzjF8EcZ9ipu9U2AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        graph = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def graph():
        
            """
            This function provides an ANSI text graph of the local repository
            """
        
            graph_msg = executor(["git", "log", "--graph", "--oneline", "--decorate", "--all"])
        
            return graph_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        graph = graph()
        
        return graph

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_7(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Branch List", "Branches", """Lists all the branches in the local git repository""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("103f8be5-992a-4026-8a1c-af7c4790d05a")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "check", "check", "Refreshes the List (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "branches", "branches", "List of all the branches in the git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGoSURBVEhLzdRLKAZRGMbxkZAUK7dERMglZcGCpKQICWVBVoqiLCwUyUoSxcrGRinZC8mejaIol+QSIRbkHin+zxzKcs5nvvLUr94z03fmm3PeM85/TTwKTOl/ynGDWywiEr5mB0OIwh3aEHCK0I4Yd2Syhmnk4hHVCCj64TOusY9YKFk4wAcmdIGkINqU3rOFKVO6kzWZ0k0LdF+ZxSv0Ryp1wWuGcYFJaK3jkIdsDEBLlY9PpGEEe/CcEIxCE1RgHE/Qw95Qh2Tofj3msQ6rJOEErbhHOjK+60IoHdBDdpGpCzbRhp5hEL9f/xxq1Sp3ZJar15R20SE6xhwOsYJtPECbqj1SIyxhDNbR5mmztUzqFC2FxuoineZ+6G10vwdWycEVdAZWoSXQwSqGsgC17zJ0XlJhFU14iTJoonBoH37Og9pVb6TJO3XBNuqgTagldWLVtqeohTID7UupOwowYdBbdLsjxzlCA/qgf6/v0Z/TDE2miTfwAj2oBL6lC2rNd6j/Q+F7EqHW1GcjaFG/N5oyONGG//5s+x590GpMGZwkIMKUXuI4X1acZKfIe0wWAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        branches = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def branch_list():
            """
            Returns a list of existing branches
            """
            
            branch_list_msg = executor(["git", "branch"])
            
            return branch_list_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        branches = branch_list()
        
        return branches

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_8(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Select Branch", "Select Branch", """Selects the a git branch""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("f53dcd2c-23be-4e85-8f7f-68b93957fdf7")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "index", "index", "index of the selected branch inside the branches list (int)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "branch", "branch", "The selected branch")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "branches", "branches", "List of all branches inside the local git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAH2SURBVEhLrdVNSBVRGMbxsTSij01Jq4KKICFsVVBrIxSKQGqR5cc2wp0IRdA2so3SByS6chHtolbixk1FkWjRTsGNn0SIpRZJ9X/Oue84jjN3jnAf+ME5M2fOO3PvnDNRRnbiBGpdr8K5jBn8K+nDDlQkp6FJX6MJXaV+DyqSAcz5Zpz7+Iu9rrcR/Yy38BKPcByFeYNPvhnnKvQUB13PZxdGoOOfsYxfOIuy6YAuuuh6UXQAXzCGKh0opRMad971/NPpxr4iOW5LdPIFdPEHzGIRp5DMMN75Zhx7Ut1U2dTgOzRY2pDOcyz4ZpyH+I3drlcmezAPK3AD6ZzEH+hta8Y9aOxdFGYfdHdWoBVZaYCNkacISmgBLT79PzbuEoISWuAQ1mDjtAMEJbTAbdgYqUNQigocQTe0sGzMBIL3q3SBFigP8BErsHPmCoKTLnATit7x5KTmDrYVLfusn2gJdmwd2osuIC8qfM43N0fbxTfYZNehvMcztEMLrVxs26h3vVSeQCcn8QNTOIpqhOQYdL2KbMk12F1rv9fE0xhFXrSiG33TXaPxj10vI68w7ptxVExF83ZJ/Uc6fxiD0CubmyHoDpKxz+Z+18tOL35Cm6RWeG70r2syfTrPQK+o+v0oylsErQd91VahiUUfoMI9nuR8yaLoPykulh6mcBQtAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, index):
        
        branch = None
        branches = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        
        def branch_list():
            """
            Returns a list of existing branches
            """
            
            branch_list_msg = executor(["git", "branch"])
            
            return branch_list_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        branches = branch_list()
        
        raw = branches.strip("\n")
        raw = raw.split("\n")
        branch = None
        branches = []
        for i in range(len(raw)):
            raw[i] = raw[i].strip("*")
            raw[i] = raw[i].strip(" ")
        
            if i == index:
                branches.append( "> " + raw[i])
                branch = raw[i]
            else:
                branches.append( "  " + raw[i])
        
        return (branch, branches)

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_9(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Create Branch", "Branch +", """Initializes the git repository (git init equivalent)""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5925fe4c-66e3-4357-a0ad-64e409297401")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "name", "name", "The name of the created branch")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "create", "create", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIASURBVEhLrdVPSBRhGMfx0Uyi8pLRKaE0MCg8KeQ5CaJCkDxoal0jukmgCOFNUjpEGRQFQofoFglC1KEOKkVSireCLqZFSBT901C/v3nnGWfX2Z032B984H1m333fmdmdZ4KUbMMh7A2rEucMFrAeuYFylCQN0KJPcBK9UT2MkuQeFt0wzlWsYVdYbUa38SIeYQS1yMw43rhhnLPQVVSHlUslnkHHZ/Edf9CEorkAfelEWAXBHsxhBmU6EOUyNK85rNzV6cTmkZy3JfrwIfTlV/iELziCZJ5iyg3j2JXqpIpmO5ahydKD/NzBZzeMcw1/sSOsimQnlmAbnEN+6rEK/dvaMADN7UdmdkNnZxt0Iy3HYXNkFF7x3UAPn34fm3caXvHdYB9+w+apA3jFd4NLsDlyGF7J2qAGV6AHy+a8g3e/yt+gE8oQXuMn7DPTCu/kb9AFRf/x5KKmD/8VPfZpt+gb7Ng/qBe1IJkxDLph4ahdfIUt1gFlGrdxHnrQ0jKJ+25YOLeghd/jBz7gACqQFnVWXbW8hFq+1Wo7OWmHnbX6vRb+iBcolOtQuxbdupVErfdFTh7jrRvG0WbatFCXPIpTEb0bJhL1QeTkAXTGydhrsyqsiuc5brpheo5Bi+k+NkJ/UdV34RP9Bplz9Vb7BS0segFl9vgoddjvhpYg2AAgGZq3nDfvtQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, name, create):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def create_branch(name):
            """
            creates a branch with the given name
            """
            
            cb_msg = executor(["git", "branch", name])
            
            return name
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if create == True and name != None and not(name.count(" ") or name.count("\n")):
            r = create_branch(name) + " created"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the create button to create the new branch\n"
        if not name: help +="\n* You need to enter a branch name first\n"
        try:
            if name.count(" ") or name.count("\n"): help +="\n* Branch name can't conntain spaces or new lines\n"
        except:
            pass
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_9"]
        except:
            rsc.sticky["Githopper_9"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_9"] == None:
            rsc.sticky["Githopper_9"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_9"]
            rsc.sticky["Githopper_9"] = None
        
        return (report, help)

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_10(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Delete Branch", "Branch -", """Deletes the selected branch""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("7969bfdf-6b54-42ea-ae60-3b84b9bed134")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "The name of the branch to be deleted")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "delete", "delete", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHXSURBVEhLrdU9SBxBGMbxjUYRjY2KnRBFMKCkMmBqgyBGBImFH1FbEbsQUIS0osFCSAKKnYXYBVNJmlQJEcUP7BRsYqKIiKImRNT/s3uz7p17t6PuAz+Y2Zubmb3bfccJSTYqUeL2Yk4zfuEyYQJZiCVPoUnn0Yg3if4YYsk0fntNP+9wgQK3dx39jH2Yw3tUIDJfsOQ1/byC7qLY7XnJxVfo+hqO8BfPkDG90Jca3J7jFGEdy3igC4kMQOOeuz3v7rSxDQTH3Yg+nIW+/BM72EM1glnAd6/px9ypNpUxOTiABks3UjOJXa/pZxT/kOf2MiQff2AW6ERqqvAfetpaMQyNHUJkHkG7Mwu8RljqYcbIR1jFdgG9fPp/zLiXsIrtAqU4gxmnCmAV2wX6YcbIE1glaoEyvIVeLDNmFdb1KnWBDigjWMQJzGdGC6yTukAXFD3jwUmNQdwqeu3DfqJDmGvnUC16gVtH5WIfZrJ2KD/wCT3Qi3bnfIAm3sQxtvAYDxEWVVbddRiVnaS0wexa9V4Tb+Mb0mUcKtdhdF4k5TNWvKYfLaZF01XJGjSlUY6kzEA7DsYcm4Vu756pgybT0VkLPaLqTyG26FQ7hSYWHUCRNT59HOcKPV2S9nGltHoAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, delete):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def delete_branch(branch_name):
            """
            deletes the selected branch
            """
            
            db_msg = executor(["git", "branch", "-D", str(branch_name)])
            
            return db_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if branch != "master":
            if delete and branch != None:
                r = delete_branch(branch)
        else:
            r = "master branch can't be deleted"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the delete button to delete the selected branch\n"
        if not branch: help +="\n* You need to enter a branch name first\n"
        help += "\n* You can use the 'select Branch' component to choose a branch\n"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_10"]
        except:
            rsc.sticky["Githopper_10"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_10"] == None:
            rsc.sticky["Githopper_10"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_10"]
            rsc.sticky["Githopper_10"] = None
        
        return (report, help)

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_11(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Switch Branch", "Switch Branch", """Switches to the selected branch""", "Githopper", "Branching")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("5834f036-cb2a-4063-8a54-71220e8479c2")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "The name of the branch to switch to")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "switch", "switch", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHBSURBVEhLrdQ5SB1BHMfxlRgjIkQtUqiFjQeoqEmhkMZOCwshiBKwFOzEUsROxBSCaBK0UIQIgiBYGWJjYSpBRDwgHqDghYWFZyBi/P529m0my+O9fbo/+LD/YWGO3ZlxEiQbxd4z8nTjFn9xgy5Elo9Qx8NoxIjXbkUk2cZ3U/r5gU1T/pc89GEWPXiNpDmHZm9nFKem9JOPQ2h1695zF2+QMOPQ9y9xW45Thjt8dVv/MoMLFLgtxynCFSbcVoLkYg3XWPGeq8iBHXU+aEo/n3FiysSpgpYcU4FgNrBoSj/L0KSSphr2AJUIphl6NwntsGmvrZ2XNG9hD6AVxUs7jvAbB2hDqIQdIBatMMOU4RIcQO1gMtGAb9DWrkfo1EAd30M7I3iAtDV1+OxJ6KyEznv8RLyZK9pVOu32APoX6QgVzfiFKd28wgdMYQtamd35H08TUo4uvx3YHdp026rjUqT0H15Cezxep6ITruuiHCknDQsIdqor5BNaUIgnJQtLUId73lN0qCLJEB5QC/3oOlxC930kOcMXU/oZw7Epn599zJnSzzx+mfL56YS+uT7JO/R67Q5ElgHEfq704wlxnEeE1IQWPBXTOAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, switch):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = "You have successfully switched branch\n\n"
                out_put += check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = "You have not switched branch\n"
                out_put += cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def change_branch(branch_name):
            """
            switches to the selected branch
            """
            
            cb_msg = executor(["git", "checkout", branch_name])
            
            return cb_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the switch button to switch to the selected branch\n"
        if not branch: help +="\n* You need to enter a branch name first\n"
        help += "\n* You can use the 'select Branch' component to choose a branch\n"
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if switch and branch:
            r = change_branch(branch)
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_11"]
        except:
            rsc.sticky["Githopper_11"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_11"] == None:
            rsc.sticky["Githopper_11"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_11"]
            rsc.sticky["Githopper_11"] = None
        
        return (report, help)

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_12(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Commit List", "Commits", """Lists all the commits in the local git repository""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("47998cf2-1c23-41cc-b9b3-7a0d5903cb1d")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "check", "check", "Refreshes the List (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "commits", "commits", "List of all the commits in the git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAG1SURBVEhL1dU5SB1BHMfxjUcRg1iosdIoBkTBwlpUvC0tJGoiJATBAy0NYpdYWNlYKmgr4tWLgoKBRMVCSYpESTSgkiJ4JhYav7/ZebCI7wDnFf7gw5v/MDuzu2931ntoSUQunpjKcRrwA/9xjE44Sz4u8R3vsAwtVAsn6YUm1O0J5QzTfvP+GYUWKDCV5yXjApOmiiFJaEU/ytRh04wv0ORygCFs2rocUZOGjwhNIhNYs+1dvEAltmzfL7xCTNEZ6aCXeIYxW+/jNfRoBpOJ230Rs4FvftNEE2iBdlM5yDiuUYJH6IMWqIGT5OEImvS3/Z2F0+RgGPM4xwLiljboKvTGxi1TuEIXGpEKp6mDriLkJ4oQNXrFs/xm2GjMV2jnrEA9TrEOPWVh8waH0BltI7glBJMOjekxlZ8PUF+Gqe5IFTTgMwahPUW7oXZHXVEp9GKN4BM0NriRLUHjH5vqjsxAl5lgKs8rhCb5Z3+DdHsWbXsHe7bdjbCZw4nfNHkOHaQN7T2aUAxtfKG8xSr0cWlRR6Toj9KEKxiAnoq/eApn6cAfaCF9+qrhPCnIRsTHLfZ43g3RfG3n8GC5mgAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, check):
        
        commits = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def log():
            """
            This function provides a log of commits
            """
        
            log_msg = executor(["git", "log", "--oneline"])
        
            return log_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        commits = log()
        
        return commits

from os import listdir, getcwd
from os.path import isfile, join
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_13(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Select File", "Select File", """Selects files in the working directory""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("87a30863-64e1-400a-bee4-ae5318fc4aeb")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "indexes", "indexes", "Indexs of the selected files inside the directory (int list)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "select_all", "select_all", "Determines whether all files should be selected (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "files", "files", "Selected files")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "directory", "directory", "List of all the files inside the current directory")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFeSURBVEhLxda9LwRBGMfxEYVONFQaCZWXgkanEK8NBYcgEcR7o+MPEFpC6x9QSpQq0aIRhYJOoqXm+5szyVnP2h17iV/yye2zmblndye3c+6/UsIZLiNo/CQys4+PAvaQmi5o0D260RihBw/Q/A6YWYUGLPgqPkvQ/GVfGdmABmgN/pIZaL4u1Mw6NEADlVHs5DACZRaav+IrI6HBlK+ce4LqLI9Qwh1kNgh30IbBHFqhzCGqQWwWoflbvjKSfEQXeM/hHEofXhHW5EdCg2lfOXeCW9xkOEJIw9enmaKPKDPJBgPYNqyhHtFJrsEzVFv0G4lO8g7aMW4YQh2iU6012EVv+fB7qtFgAvqOTl8lUrRBCzRfTcxsQgPyvk37MVw+dLXQu+vYVymJ3Q/mofHNOMUdfk3ljqYdqnLH0hVaOcQbXtCkE1lJ25OvUAMr1xgrH+aL9a/iAGkNUs479wkCEpLaMnJeZQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, indexes, select_all):
        
        files = None
        directory = None
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        mypath = getcwd()
        f_list = listdir(mypath)
        
        try:
            f_list.remove(".git")
        except:
            pass
        
        if len(indexes) == 1:
            indexes = indexes[0].split("\n")
            indexes = [i.strip("\r") for i in indexes]
        
        temp_list = []
        for i in indexes:
            try:
                temp_list.append(int(i))
            except:
                pass
        indexes = temp_list
        
        files = []
        directory = []
        
        for f in range(len(f_list)):
            if isfile(join(mypath, f_list[f])):
                if f in indexes:
                    files.append(f_list[f])
                    directory.append ("> " + str(f_list[f]))
                else:
                    directory.append ("  " + str(f_list[f]))
            else:
                if f in indexes:
                    files.append(f_list[f])
                    directory.append ("> " + str(f_list[f]) + " (dir)")
                else:
                    directory.append ("  " + str(f_list[f]) + " (dir)")
        
        if select_all:
            files = ["-A"]
            directory = ["> " + str(f) for f in f_list]
        
        return (files, directory)

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_14(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Commit Changes", "Commit", """Commits the changes to the selected files""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("d4a9b289-3f73-4888-a8c9-37d4717c2905")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "files", "files", "List of the selected files")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "message", "message", "commit message")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "commit", "commit", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFCSURBVEhL7dVNKwVRGMDxKSG5ZaNs5CV1N3wIKxsLISUrO1n4DK7CQqLESkjZ+ASyIAnbW9eNBVtlobwUCwn/55559JgOMi8L5V+/7pmZM2e6c2e6wX9/pnbM4hhnOMI0WpG4EdzjzeMWQ4hdD3wLR3UjVpfQRU7Rj04MQm6VHjvHt9VCbsWoIfdYF7hCI2xNuIbOKcCeP4xqVJKTdaLPPHwtwTdfvKABlX66wCR8zcA3X3y6QA4r2DB2oZOL8FWGztmBPV++XR2+rAZ30AW20IIqtGEbeuwGsv/XTUAXEY+4wJPZJ8YQu0XYxaLmkLgBHOABr+HnPvqQavLs58PPaJuYcsNsOsG6G6aXPGn1oUOsme2PtzhJC5DfQ8iL9Wy2x5G4LvSGSpCXTbflPyTV9rDshtkkv8GqG2ZTB5rdUAuCd53UgEObnuwGAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, files, message, commit):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def commiter(msg="No comment", f=[]):
            """
            This function saves the selected portion of the gh file from clipboard
            and commits it with the given massage
            * files: a list of file names that will be committed
            * if files contains "-A" then all files will be committed 
            """
            
            commit_msg = "" 
            
            for i in f:
                try:
                    executor(["git", "add", str(i)])
                except:
                    commit_msg += "Could not add" + str(i) + "to the repository\n"
            
            commit_msg += executor(["git", "commit" , "-m", msg])
            
            return commit_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area + help ------------------------------------------------
        
        help = "Press the commit button to commit the changes (to the selected files)\n"
        
        r = None
        if message == None or message.startswith("Double click"):
            message = "Commit message not specified"
            help += "\n* Are you sure you don't want to leave a message ?!\n"
        
        if len(files) == 0 or files == None:
            files = ["-A"]
            help += "\n* All files will be committed"
        
        r= None
        if commit == True:
            r = commiter(message,files)
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_14"]
        except:
            rsc.sticky["Githopper_14"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_14"] == None:
            rsc.sticky["Githopper_14"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_14"]
            rsc.sticky["Githopper_14"] = None
        
        return (report, help)

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc

class Githopper_15(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Modify Last Commit", "Modify", """Modifies the last commit""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("82f9bb62-e543-434c-8bc3-e2251024c695")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "files", "files", "List of the selected files")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "message", "message", "The new message to replace the last commit's message")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "modify", "modify", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFFSURBVEhL7dXNK0RRGMfxK3mZ8rJRrMwo2fgHLK1shWhSyqysbGwsWWAhpZS1DQv+AdnIAmU1aYRiqyyUl2IlfH9jnjpuh2nuHAvlV5/udO5znts8c2Ym+s+fSReWcIRzHGIBaVSdcTzi3eMeo0icAfgax/UjUa5hTQoYQi9GoFHZvQv8mAZoFJMOzdga3KANbtpxC6uZh7s/izoUo81W6LMCX9bgq5dXtKKYcg+Ygy+L8NXLlwc0YR0bjj1YcR6+nMFqduHu17tL4dvU4wHWYBOdqEUG27B7d9B6xZmGNZFnXOHFWZMpJM4q3GZxy6g6wzjAE95K130MIh6NtvnzZeXR2e8pXX3pgE7cLLq1EDItOMUlZjCGYFHzY9jnohPWiCDRl8ltvoVg0dk/wa80V/qwAxtL8ExA/3Q51GghdMr8PETRB7zNgYOR3npxAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, files, message, modify):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def amender(msg, f=[]):
            """
            This function saves the selected portion of the gh file from clipboard
            and commits it with the given massage
            * files: a list of file names that will be committed
            * if files contains "-A" then all files will be committed 
            """
            
            commit_msg = "" 
            
            for i in f:
                try:
                    executor(["git", "add", str(i)])
                except:
                    commit_msg += "Could not add" + str(i) + "to the repository\n"
            
            if msg == None or msg == "":
                commit_msg += executor(["git", "commit", "--amend", "--no-edit"])
            else:
                commit_msg += executor(["git", "commit", "--amend", "-m", msg])
            
            return commit_msg
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if modify == True:
            r = amender(message, files)
        
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the modify button to modify the last commit\n"
        if message == None: help += "\n* You can change the last commit's message by entering a message"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_15"]
        except:
            rsc.sticky["Githopper_15"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_15"] == None:
            rsc.sticky["Githopper_15"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_15"]
            rsc.sticky["Githopper_15"] = None
        
        # return outputs if you have them; here I try it for you:
        return (report, help)

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_16(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Select Commit", "Select Commit", """Selects a git commit""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("e875c5e4-7cf5-4157-b2cc-c9e1fd85921e")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Integer()
        self.SetUpParam(p, "index", "index", "index of the selected commit inside the commits list (int)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "commit", "commit", "The selected commit")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "commits", "commits", "List of all commits inside the local git repository")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAE7SURBVEhL7dS/K0ZRHMfxKyGlLGKRH4tFdqNSssmvklI2kz/AxIBBSsTKYvEXyCIDVokYGCzKoPwIk/D+nOd+67gdj9znGJR3vbq/zj33eU63m/z3Z2rFPA5whn3MohklN4oHvAfcYRi560Fo4qwu5OoSNskJ+tGOQWip7No5ilYFLcW4R2tsE1yjDn4NuIGNmYF//wgq4NLNNjBkEaFWEBovr6iF67sHTCPUHELj5dMDarCGDc8ObPARQp3CxmzDv1//rhpfVol72ASbaEI5WrAFu3YLnf9xk7BJ5BkXePHOyQRytwR/sqwFlNwA9vCIt3S7iz5ETe9+W7ot1hQ6C7vxG4KWrsMdRU5fXU2uh0SpG72FXfeaXmHVHUVqDPrFjVjHMaK3jCfow1evE7/RIaK/sn5l6TZTknwApul7qilH2ZIAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, index):
        
        commit = None
        commits = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def log():
            """
            This function provides a log of commits
            """
        
            log_msg = executor(["git", "log", "--oneline"])
        
            return log_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        try:
            commits = log()
            
            if not len(commits):
                commits = "nothing has been commited yet"
            
            raw = commits.strip("\n")
            raw = raw.split("\n")
            
            commits = []
            for i in range(len(raw)):
                raw[i] = raw[i].split(" ")
                if i == index:
                    commits.append("> " + " ".join(raw[i][1:]))
                    commit = raw[i][0]
                else:
                    commits.append("  " + " ".join(raw[i][1:]))
        except:
            commit = "No commit has been selected"
        
        return (commit, commits)

from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_17(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Reset to Last Commit", "Undo", """Resets the files to the last commit state""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("6e10f1ca-e336-4ef4-a427-a255998d8eae")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "reset", "reset", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        result = self.RunScript(p0)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGASURBVEhL7dQ/KEVhGMfxEwax+DdhMAlRyGZmQQy6FsJgMzBZTCgrSgrFrJBFjMpwS/lbyiYDi5KN/P3+7jmvnm73XF333jLcX33ynvc89xz3fd77erlkKnko8IfZyRz6/WHmU4o3HGMWW1jHEAqRdubxFeIRffhz6mEf+IF76FtMYwZ76IX6lHI6cAP3gmsUIz5NKPKHqScfPdB/+oJmZC2taPGH6aUK7aiLXf0e9Ur1+lzSaDmW8Aq37vsI+2A1DuBqtYQLCG34MlT4jiM8BNfniI+afQXd185SvXaZrhfxk1p0YRC6+QSttVKGE2heW1J13WhABJqPogRKG57xiRpoF8bepkJHe9xmDPa+bGAqGI/CZhea7wz+egPYxmEwcQmbVWj+DKrbwQjGofkV2Oi3onl9m01N2FxAN9XYYajhutZZVAkbLa1bczVW9a7hp0h4+jbiDipy9HD1J1H0UG0IW38L9Sg0FZjEGnR66qXJomNCx7nqJ1COXP5NPO8bpHNvgYCkaAcAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, reset):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except:
                pass
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if reset == True:
            executor(["git", "reset", "--hard"])
            r = "The repository has been reset to the last commit"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the reset button to reset the project to the state of the last commit"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_17"]
        except:
            rsc.sticky["Githopper_17"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_17"] == None:
            rsc.sticky["Githopper_17"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_17"]
            rsc.sticky["Githopper_17"] = None
        
        return (report, help)

from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_18(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Hard Reset", "Reset", """Resets the repository to the selected commit (deletes the commits after that)""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("b5e00fd3-ebff-4412-bd2c-127a572b586b")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "commit", "commit", "The selected commit to reset to")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "reset", "reset", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAICSURBVEhLzdZNSBRhHMfxTbuIGVSiFUpQYQmaLxHUKRI8dCiJIjCiSycRRPQodBIh0oN4sG4JitHBWwUZ6aFEi+oQBF16IYTQk6CoiOj398w88jg7Mzs7XvzBh33+szvP4+zzsmb2UwpQjlMowwGkzgX/VWnBOOax5fiHUdxA3vmGZ/gA2+EfvMEL//Uv7HtfcA2JUoF16MYNDKEBwegrasQw7EDdyJlW2Bt+60Igtajzmju5DH020SCayNtoQy/OwM00PnvNXTmJX9AgV3Uhbd5j1mtmpR4a4CcO6oKbW/iO86aKzjvMeM3QDEKD3DGVk5fQG9Wmik6uAU5D/bwylZOjuOI1Y5NrAOUHllFkKlKMJ7hoqvhoD0TNgY02oJ5CT2NiJ2fEVNG5hAWErSI32jvqr8ZURE/Qh+D6ttHRMQHdpBVyE3F5Dn32rKn8HIc2jJtzGIM+vAjtjazlF5KvWMMhU/l5C3Wk01LpgOoldGFnwnLkBDYxZSon96FDzo6q3dyDElMlzyPoD3toqkAKoQ2n4yJNKrGC/9C8ZqUKGv2TqfKLvsI56P67uhAWPcEAnuIwjiFJNG8foc51VCTKa6yiyVTh0U+njmft2rw6V+5BW74Z7ZiEHew6dGRotahjbb4HSJ1+qCOtKuUxVGuuOnEEe47mw/4nobkq9ZpxyWS2AUWkb9la3Eq8AAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, commit, reset):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except:
                pass
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        if reset and commit:
            executor(["git", "reset", "--hard",  commit])
        
        # Help production area ---------------------------------------------------------
        
        help = ("Press the reset button to reset the project to the last commit state"
                  "\n\n* Warning: this component is dangerous --> All the changes after "
                  "selected commit will be erased !!!")
        
        if not commit: help += "\n\n* Please first enter the selected commit"
        
        return help

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc

class Githopper_19(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Revert File", "Revert", """Reverts the selected files to the selected commit's state""", "Githopper", "Committing")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("31ba183a-aab7-4305-a4cd-a800a0c4e877")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "commit", "commit", "Selected commit to revert the files state to")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "files", "files", "Selected files to revert")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.list
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "revert", "revert", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFaSURBVEhLxda9LwRBHMbxEQWVaBR6GkRBRKkQhErj5UIhiHeFTqIWOonEXyE0EqVKTyUkCmq1mu8za5LN7uzOjEt4kk9uf8lvMjs7dztn/ivzuMRdAvXPIZgTfDXhGJUZhJqeMISuBMN4hsYPwJtNqGHFVulZg8av28qTHahBe/CbNKDxulFvtqEGNSozOIwwDWUJGr9hK0/cBAu2MuYNqkNeobgVBCdwK+jFZIQeKMtImiA1q9D4PVt5UnxEt/iMcANlDB9we1KKm2DRVsZc4BEPAedw6fz59KbZRxRMcYIJHHhsoQPJKe7BO1T76DeSnOIK+jHrMYU2JOfP9yA2+xjJLuuTOoEe0xE0RgeO9q4VldmFmmPfpuNQf94LuuFN6nmgu9XXVmPOoNf9Fa7RjlLyJ5pOqPyJVbd0vXtGs0sbvTL6sstyqs7ke7QgNrV74ftXcYqUCYgx37zrk+qH0M/bAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, commit, files, revert):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if revert and commit and files:
            if files[0] == "-A":
                r = "You can not revert all files (you can use \"hard reset\" component for that)"
            else:
                r = ""
                for i in files:
                    try:
                        temp = executor(["git", "checkout", commit, str(i)]) + "\n"
                        if temp != None or temp != "":
                            r += temp
                    except:
                        r += "Could not revert " + str(i) + "\n"
                if r == None or r == "":
                    r = "revert oporation finished"
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the revert button to revert the selected files to the selected commit state"
        if not commit: help += "\n\n* Please first enter the commit"
        if not files: help += "\n\n* Please remember to add the file names"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_19"]
        except:
            rsc.sticky["Githopper_19"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_19"] == None:
            rsc.sticky["Githopper_19"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_19"]
            rsc.sticky["Githopper_19"] = None
        
        return (report, help)


from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc

class Githopper_20(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Merge Branch", "Merge", """Merges the selected branch into the current one""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("87678394-2346-420c-a93a-583036334ec7")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "The selected branch to merge into the current one")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "favor_this_side", "favor_this_side", "Determines whether to resolve conflicts by favoring this side of the merge (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "manual_resolve", "manual_resolve", "Determines whether to leave conflict solving to the user (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "merge", "merge", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGJSURBVEhL7dTLKwVRAMfx8SzkvcLCyj9iI1mIrJCtYsPCQiGPhSIUS1KyFoo/Qjb+Ayslb0JZeHx/c8+pc905Z1xZUH71aebM/Z153Dv3RL81g2jM7H4v7RhDWzzKzjTeURmP8kwBtqETWJuwGYeO3aMBZcgr3dAJptCMOTNuxZDZl1ec4wzHUP9LT7QMncBGT/SCI9iT+5ygHsH0QuVh1GLEjDsxYfblDY94do7JGoIpxj5UvjLbHdgsQsfu0IImLJhjcgqdI5hq6O7siSrgZhX6rDweRVEVnqBj19D8YPTV3EITLpH04+lt0t0rn/upF9APpTvXBH1NvgmFZuv2f/QCNv8X+IMXqIM7Qe95KHpNbf8Caf34j/UATbhBKUJx+/qjBfta3LagshY5bTfgS1J/Hd50QaVJaLmeMeMOJMUu71oI1Z81Y18/Z7lWNJ7P7OZkBW5fTxTqZy3XNbDLdQ+S0ge3P2rGvn5UggOoZO2hCElR/xBufxe+fhw95gCW0K8DKQn0o+gDqOGdjVphp3YAAAAASUVORK5CYII="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, favor_this_side, manual_resolve, merge):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        
        if branch:
            help = "Press the merge button to merge the selected branch into the courent branch\n"
        else:
            help = ("Please enter a branch and press the merge button to merge the "
                      "selected branch into the courent branch\n")
        
        if not manual_resolve:
            help += "\n* Merge conflicts will be resolved automatically\n"
            if favor_this_side:
                conf_manager = "--strategy-option=ours"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring this side of the conflict")
            else:
                conf_manager = "--strategy-option=theirs"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring the other side of the conflict")
        else:
            conf_manager = "manual"
            help += ("\n* Conflicting files will be altered\n"
                      "\n* You have to manualy edit the files and resolve the conflicts"
                      "\n\n* After manualy resolving the conflict make sure to use "
                      "the \"Conflict Manager\" component to either resolve the merge "
                      "conflict or abort the oporation")
        
        if merge and branch:
            if conf_manager != "manual":
                executor(["git", "merge", "--no-ff", conf_manager, branch])
            else:
                executor(["git", "merge", "--no-ff", branch])
        
        return help

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc

class Githopper_21(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Pull from Repository", "Pull", """Pulls the remote repository changes to the local repository""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("97c47f69-1430-4e51-847d-aa5a6d106e11")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "Name of the branch to be pulled")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "favor_this_side", "favor_this_side", "Determines whether to resolve conflicts by favoring this side of the pull (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "manual_resolve", "manual_resolve", "Determines whether to leave conflict solving to the user (Toggle)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "pull", "pull", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        p3 = self.marshal.GetInput(DA, 3)
        result = self.RunScript(p0, p1, p2, p3)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGjSURBVEhLrdXLKwVhHMbxQy5ZiHIpKWyspBQlKckKGyvJVtnZi4VSbokNWxui1Cm5S1IWSMoCuWzc/gaJlMv3mZmXk46Zd845T32aeX/n/c2ZOb3znkgCyfCOKU07FnCOe+84j1YklWJs4cvHGgoQOmq6RryL/nWBfITKCtQ8hSasQnc7h3Xo80bMQvOWYZ0GmLvrV8EnQzBz61SwibmrD7Sp4JMOfELz9bRWOYAabp1RcO6g+XvOyCKnUIOWo01uoPlHzsgiu1DDCwpV8EkJXqH5GyrYZBhqkCjSES96q5dg5g7CKpVQwwyO8YQxZEPJgVbPJczF31EO60ziDVp6WuPTME+io14uc3HRF4aOflOtpG7UqBAT8yLKogqJZgK6yKEz+s0+njHgjJJMBWrd059oXOaehk8pmt1T62i+lmxgsqAXTD/LqAoWGYfmnyFTBb+koQUPUNMm/nvZirADzdN2oadQv1XUvA0161+sHrHRjvuIoJsIjHl86VGB9MLURlRINl0w+82Jd9Q+1YmUpRpX0MW1RVQh5clDH3KdUWAikW894HrsUOMkFAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, favor_this_side, manual_resolve, pull):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd)
            except:
                pass
        
        def puller(options):
            """
            pushes repository to server
            """
            
            executor(["git", "pull"] + options)
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area & help ------------------------------------------------
        
        if not manual_resolve:
            help = "Merge conflicts will be resolved automatically\n"
            if favor_this_side:
                conf_manager = "--strategy-option=ours"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring this side of the conflict")
            else:
                conf_manager = "--strategy-option=theirs"
                help += ("\n* In the case of a conflict it will be resolved"
                           " by favoring the other side of the conflict")
        else:
            conf_manager = "manual"
            help = ("Conflicting files will be altered\n"
                      "\n* You have to manualy edit the files and resolve the conflicts"
                      "\n\n* After manualy resolving the conflict make sure to use "
                      "\"Finish Conflict\" component to either resolve the merge conflict"
                      " or abort the oporation")
        
        pull_options = []
        
        if branch == None or branch == "": pull_options.append("--all")
        
        if conf_manager != "manual":
            pull_options.append(conf_manager)
        
        if branch != None: pull_options.append(branch)
        
        if pull:
            puller(pull_options)
        
        return help

from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs
from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc

class Githopper_22(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Push to Repository", "Push", """Pushes the local repository changes to the remote repository""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("97deeaa3-1d5d-4c69-849a-17b1113837e1")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "Name of the branch to be pushed")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "repository", "repository", "URL Address of the remote repository")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "push", "push", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGiSURBVEhLrdTLK4RRHMbxIZdsEFI2bmUrRSRlp7Cxlo0s/AtioWzcosTWhigZyXUhkQUWVi65lCg7e8klt+/zvu/hTdM7Z2bepz6d95w558w70zm/SBLJ8NpQ0455nOHea+fQipRSjG18B1hHIRKOFl0h1qb/nSMfCWUVWjyBZqxBbzuLDejzJsxA85ZgnUaYt+vTQEAGYebWacAm5q0+0aaBgHTgC5qvX2uVA2jBjdOLnzto/q7Ts8gJtEDH0SbX0Pwjp2eRHWjBM4o0EJASvEDzNzVgkyFogUSRjljRrV6EmTsAq1RBC6ZxjAcMIxtKDnR6LmA2f0cZrDOOV+jo6YxPwvwStbpcZnPRFyYc/ac6SZ2o0YAv5iLKggaSzSi0yaHT+8sentDv9FJMOWrdx9+oX+o+hpsWrw09qq5b0N+lYleA0FIPUw4evfYW1sUtKD1Q0dOmI1DdH/P6H+hGUtFZ10XTRroPOqr+dOEN+nwKabBOJUxFvUQ1YkV3wxS6fVQgbrJgSsAychGUPKxA80+RibhpQK/7aB3N12HwJRL5AetketrxxHLdAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, repository, push):
        
        help =None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd)
            except:
                pass
        
        def pusher(options):
            """
            pushes repository to server
            """
            
            executor(["git", "push"] + options)
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        push_options = []
        
        if branch == None or branch == "": push_options.append("--all")
        
        if repository == None or repository == "":
            push_options.append("origin")
        else:
            push_options.append(repository)
        
        if branch != None: push_options.append(branch)
        
        if push:
            pusher(push_options)
        
        # Help production area ---------------------------------------------------------
        
        if branch and repository:
            help = "Press the push button to push the selected branch to the selected remote repository\n"
        elif branch:
            help = "Press the push button to push all branches to the selected remote repository\n"
        else:
            help = "Press the push button to push all branches to the remote repository\n"
        
        return help

from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_23(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Force Push", "Force", """Forcefully Pushes the local repository changes to the remote repository""", "Githopper", "Merging")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("0270722b-cc28-4415-b95e-a2a0b7f5f3c2")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "branch", "branch", "Name of the branch to be pushed")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "repository", "repository", "URL Address of the remote repository")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "force", "force", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        p2 = self.marshal.GetInput(DA, 2)
        result = self.RunScript(p0, p1, p2)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAIYSURBVEhL7dVLSBVhGIfxKU2MsNI2ZffosolIiBQXdm8RigTZhUishW3cuBKhRUt3hitdFS3DqGgXoeVCxIgCkaTbSqJlpEFiUc9znA/mTGPH1GV/+HFm3vnmPTNzvm9O9D//kn14gbO5vT+zAxfRFn9uR1bOwT57cnuJ1GAWv3DJQpzV6MMMPBZ8Ry9KEXIZHnPsYQvpHMBnOCjcyRCSjdMGYbxy9z9hv4X5shcPsBk34Uk+kqPowNX4sw7him9gKzxvNxaUMkzDBkcsZOQ4PP4VayxkxWfYgzsJ61ELT55AEbJSjHdwXDUqkOxzC9FaTMFBwRacjLdH8be8hOOOwZmV7PMF0Qpsgs9cbptDcNBPzDclt+EbHFdlgSR7bbSQFa/G25/EKwzDqesjMOVowGvY/AN8jJ5XMP4enlSPC3iLdjxHmCEH4ZjgDBrj7W5kxqu6Cwc9QSWMi2wAnXDRGW8/NO+yQKw9hbXbsF9eTsOD95GeNdfh47CJ8cv9UtdHMj7Wh7DPCQvp+CUOWkpWwT6Lzqn4c9mzAY/h7T9CmFHLEt+MH2Hz4D1cK0vONbjYbOp6cHsk3v+BFiwqKxHWhO9+53p4ffgjuk7Cf4TvHN8IC84uPIMnj8P/CdMEa+dze3ML7g2sOW13omBKMAZPugdfhiE2tu4KD1mHflh3rThNC8ZXb+vcZl6uwEbNub38OD71NxlFvwFUSYtnC9WIiQAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, branch, repository, force):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except:
                pass
        
        def pusher(options):
            """
            pushes repository to server
            """
            
            executor(["git", "push"] + options)
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        push_options = ["--force"]
        
        if branch == None: push_options.append("--all")
        
        if repository == None:
            push_options.append("origin")
        else:
            push_options.append(repository)
        
        if branch != None: push_options.append(branch)
        
        if force:
            pusher(push_options)
        
        # Help production area ---------------------------------------------------------
        
        help = ("Press the force_push button to replace the remote repository with "
                  "your local git repository"
                  "\n\n* Warning: this component is dangerous --> It will completely "
                  "wipe out the git history of your remote repository !!!"
                  "\n\n* This component will not effect your local repository")
        
        return help

from subprocess import check_output
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_24(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Conflict Manager", "Conflict", """Finishes the conflict resolve operation""", "Githopper", "Utility")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("c254d51d-d235-46a4-a0e2-1a7a63e50a1f")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "resolve", "resolve", "Ends the merge operation (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "abort", "abort", "Aborts the merge operation (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "report", "report", "Output of the git operation")
        self.Params.Output.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Helpful tips about the git oporation")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            if not hasattr(result, '__getitem__'):
                self.marshal.SetOutput(result, DA, 0, True)
            else:
                self.marshal.SetOutput(result[0], DA, 0, True)
                self.marshal.SetOutput(result[1], DA, 1, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAHWSURBVEhLzda9L2RRHMbxs14jIQQbBEviJYRslixREIVQbbfK1WjRiLeIBPGSbLNLZ3UKhUro/BEaNEhsIhQU6w9Q2O9zZk5mcs3LuTOReJJP5v5+c8+9mXvPPXdMyAxgHX22eoMs4wUztsoiFdhFv61imYVOMGGrWIawgzJbeeQHdKAHtKgRzTzUn7RVJJ34B/W/q+GTHGxDg/6iGUrwF7TjDur9xAeEyh40+NBWxpSjDboUOtgJ9P0fZJxNtEY2X6UDG5HN8KmOfvqmKvrplRE8YcFW6bMK3ehBW3nkG3RtZVqNFFmE9nvGsBq+6YGmaaqTuIPf47MaiaI5fxxwhH3cwP2SJeRBKcAa3HfX0P4aFzyW2YLbMZUrFEPRNL1Fov2CTC2+BnyBLtEZtNM5ahCfelxC35+iGxoXPFbC5MI9ZDp4silYB3cSrV3eT7LWGg26QLr5rZPoHmj/cTV8UoQVNNgqfbQgaikvtNV7iu7Fb2hJTpQu/IpsZpYD6Nq61fQjNFMqEb+aakKESj60BGuwZsknKO6FM2UrY5qg94V6en+4BzFtxqBBWgIa1YhmDurHv9G0lD9C/VE1fFIKPeG9tool2TtZ/zZ0L0pslUVC/qsw5j+9LnlCUMbwHAAAAABJRU5ErkJggg=="
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, resolve, abort):
        
        report = None
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                out_put = check_output(["cmd", "/C"] + cmd, creationflags=0x08000000)
            except subprocess.CalledProcessError as cpe_error:
                out_put = cpe_error.output
            out_put = str(out_put, "utf-8")
            
            return out_put
        
        def finish_merge(abort):
            """
            Finishes the merge process by continuing or aborting the oporation
            """
        
            if abort:
                try:
                    fm_msg = executor(["git","merge","--abort"])
                except subprocess.CalledProcessError as cpe_error:
                    fm_msg = cpe_error.output
                    fm_msg = str(fm_msg, "utf-8")
            else:
                try:
                    fm_msg = executor(["git","merge","--continue"])
                except subprocess.CalledProcessError as cpe_error:
                    fm_msg = cpe_error.output
                    fm_msg = str(fm_msg, "utf-8")
            
            return fm_msg
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area -------------------------------------------------------
        
        r = None
        if resolve != abort:
            if resolve:
                r = finish_merge(False)
                if r != "" : r += "\n"
                r += "* Resolved conflicts will be implimented (check repository status for more info)"
            
            if abort:
                r = finish_merge(True)
                if r != "" : r += "\n"
                r = "The merge oporation will be aborted and file changes will be cancelled"
        
        
        # Help production area ---------------------------------------------------------
        
        help = "Press the abort or resolve button to finish resolving the merge conflict\n"
        
        if resolve == True and abort == True:
            help += "\n* You can not resolve and abort the oporation at the sae time !"
        
        # Sticky area ------------------------------------------------------------------
        
        try:
            rsc.sticky["Githopper_24"]
        except:
            rsc.sticky["Githopper_24"] = None
        
        # Report area ------------------------------------------------------------------
        
        if rsc.sticky["Githopper_24"] == None:
            rsc.sticky["Githopper_24"] = r
            report = r
        else:
            report = rsc.sticky["Githopper_24"]
            rsc.sticky["Githopper_24"] = None
        
        return (report, help)

from subprocess import check_output, Popen
import subprocess
import os
import scriptcontext as rsc
from ghpythonlib.componentbase import dotnetcompiledcomponent as component
import Grasshopper, GhPython
import System
import Rhino
import rhinoscriptsyntax as rs

class Githopper_25(component):
    def __new__(cls):
        instance = Grasshopper.Kernel.GH_Component.__new__(cls,
            "Execute Git Command", "Execute", """Executes the given custom git command""", "Githopper", "Utility")
        return instance
    
    def get_ComponentGuid(self):
        return System.Guid("fcac3693-d9ca-4079-ba22-9e0af7fb162a")
    
    def SetUpParam(self, p, name, nickname, description):
        p.Name = name
        p.NickName = nickname
        p.Description = description
        p.Optional = True
    
    def RegisterInputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_String()
        self.SetUpParam(p, "command", "command", "The custom git command to run")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
        p = Grasshopper.Kernel.Parameters.Param_Boolean()
        self.SetUpParam(p, "execute", "execute", "Triggers the git command (Button)")
        p.Access = Grasshopper.Kernel.GH_ParamAccess.item
        self.Params.Input.Add(p)
        
    
    def RegisterOutputParams(self, pManager):
        p = Grasshopper.Kernel.Parameters.Param_GenericObject()
        self.SetUpParam(p, "help", "help", "Output of the git operation / Helpful tips")
        self.Params.Output.Add(p)
        
    
    def SolveInstance(self, DA):
        p0 = self.marshal.GetInput(DA, 0)
        p1 = self.marshal.GetInput(DA, 1)
        result = self.RunScript(p0, p1)

        if result is not None:
            self.marshal.SetOutput(result, DA, 0, True)
        
    def get_Internal_Icon_24x24(self):
        o = "iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAFLSURBVEhL7dW9L0NRHMbx6y06WoxsIhGTrYnRZjH7E4xiI14Soki8bGxC4m1CCEHSKrGI0WixYjAb+D4596Zu3F97brWLeJJPek7b3Kc99+UEfyr9mMFyDUwji1j0wScKOMQVjnAZzou48aTj5BDLGk7RgnF0YQzdmECa6McsuWEpKjhGM1bQg3n0YhVpco0fBbN4wQ7WsY0NbIXz/RReMYlYooI97OIA+rJeNdf7GldiFmiJLtzw10k8B1rnE+jk3qIPUe4x6oZeucOiG5aignO04QkfWEA7NjEM35gFeTcMRqBrWYaQgS5f35gFWqJO6MAPGEAD3qCLwDdmwRk6oPVuQhTNBzEH3SNT0P1ixSzQDWKlFc94x2M4t2IW6DlULo3QP9NruVRd4Jv/gopJLNCzSJtMLZL4LIp2tO87U7USd7S678l1SBB8AUE7jhoNEhJvAAAAAElFTkSuQmCC"
        return System.Drawing.Bitmap(System.IO.MemoryStream(System.Convert.FromBase64String(o)))

    
    def RunScript(self, command, execute):
        
        help = None
        
        def executor(cmd):
            """
            This function executes the given command in the form of a list
            * It returns the output of the cmd prompt as a raw string
            """
            
            try:
                Popen(["cmd", "/K"] + cmd)
            except:
                pass
        
        def parser(cmd):
            def index_finder(text,char):
                out_put = []
                b = 0
                
                for i in range(50):
                    try:
                        b = text.index(char, b+1)
                        out_put.append(b)
                    except:
                        break
                
                return out_put
            
            a = sorted(index_finder(cmd, "'") + index_finder(cmd, "\""))
            slices = [cmd[a[i]+1:a[i+1]] for i in range(0,len(a),2)]
            for i in slices: cmd = cmd.replace(i, "<>")
            cmd = cmd.split(" ")
            
            out_put = []
            for i in cmd:
                if  "<>" in i:
                    out_put.append(slices.pop(0))
                else:
                    out_put.append(i)
            
            return out_put
        
        
        # CWD area ---------------------------------------------------------------------
        
        try:
            rsc.sticky["git_path"]
            os.chdir(rsc.sticky["git_path"])
        except:
            pass
        
        # Command execution area & help ------------------------------------------------
        
        try:
            command_lst = command.split(" ")
            
            if command_lst[0] == "git" and execute:
                executor(parser(command))
            elif command_lst[0] != "git":
                help = "Invalid command (Please only use git commands)"
            else:
                help = ("Press execute button to run the command"
                          "\n\n* make sure to put file names in quotation or double quotation"
                          "\nExample:\ngit checkout HEAD~1 'some file.txt'")
        
        except:
            help = "You haven't entered a git command"
        
        return help

import GhPython
import System

class AssemblyInfo(GhPython.Assemblies.PythonAssemblyInfo):
    def get_AssemblyName(self):
        return "Githopper"
    
    def get_AssemblyDescription(self):
        return "A simple Git interface for Grasshopper"

    def get_AssemblyVersion(self):
        return "0.1"

    def get_AuthorName(self):
        return ""
    
    def get_Id(self):
        return System.Guid("9184ee38-d815-4351-a353-c42ac7fca4b6")