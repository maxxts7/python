import copy


class VirtualFileSystem:
    """
    Implement a virtual file system with the following features:

    Basic File Operations:
    - create_file(path, content) -> bool
    - read_file(path) -> str | None
    - write_file(path, content) -> bool
    - delete(path) -> bool

    Directory Operations:
    - mkdir(path) -> bool
    - mkdir_p(path) -> bool  (creates parent directories)
    - ls(path) -> list | None
    - delete_recursive(path) -> bool

    Path Utilities:
    - exists(path) -> bool
    - is_file(path) -> bool
    - is_directory(path) -> bool
    - get_parent(path) -> str | None
    - get_absolute_path(relative_path) -> str
    - pwd() -> str
    - cd(path) -> bool

    Move/Copy:
    - move(src, dest) -> bool
    - copy(src, dest) -> bool

    Search:
    - find(path, name) -> list  (find files/dirs by name)
    - grep(path, pattern) -> list  (find files containing text)

    Size/Quota:
    - get_size(path) -> int
    - disk_usage() -> int
    - set_quota(bytes) -> bool

    Permissions:
    - chmod(path, permissions) -> bool  (permissions: "r", "w", "rw", "")

    Symbolic Links:
    - symlink(target, link_path) -> bool
    - is_symlink(path) -> bool
    - readlink(path) -> str | None

    Advanced:
    - tree(path) -> dict
    - diff(path1, path2) -> str
    - append(path, content) -> bool
    - truncate(path, length) -> bool
    """

    def __init__(self):
        self.files ={}
        self.directory ={}
        self.directory[""] =  {'parent':"",'name':""}
        self.quota= 100
        self.links ={}

  


    def create_file(self, file_path:str, Content:str)->bool:

        lst = file_path.split('/')
        if self.quota < len(Content):
            return False

        self.files[file_path] = {'content':Content,'parent':lst[-2],'filename':lst[-1],'permission':'rw'}

        return True
    
    def read_file(self,file_path:str)->str:
        
        if file_path not in self.files:
            if file_path not in self.links:
                dir,_,filename = file_path.rpartition('/')
                if dir not in self.links:
                    return None
                else:
                    dir = self.links[dir]
                    file_path = f'{dir}/{filename}'
            else:
                if self.links[file_path] not in self.files:
                    file_path = self.getfilefromlink(self.links[file_path])
                else:
                    file_path = self.links[file_path]

        if file_path not in self.files:
            return None

        if self.files[file_path]['permission'] not in ['r','rw'] or self.files[file_path]['permission'] =='':
            return None
        print(self.files)

        return self.files[file_path]['content']
    
    def getfilefromlink(self,filepath:str)->str:

        if filepath not in self.files:
            if filepath not in self.links:
                return ''
            else:
                if self.links[filepath] in self.files:
                    return self.links[filepath]
                else:
                    filepath = self.getfilefromlink(filepath)
                    return filepath
        else:
            return filepath
                

    
    def delete(self,file_path:str) -> str:
       
        
        if file_path not in self.files and file_path not in self.directory:
            return False
        
     
        
        if file_path in self.files:

            if self.files[file_path]['permission'] =='r':
                    return False
            del self.files[file_path]
        else:
            for f in self.files:
                if file_path in f:
                    return False


            for f in self.directory:
                if file_path in f and file_path !=f:
                    return False

                           
            del self.directory[file_path]

        return True
    
    def write_file(self,file_path:str,content:str) ->bool:
       
        if file_path not in self.files:
            if file_path not in self.links:
                return None
            else:
                if self.links[file_path] not in self.files:
                    file_path = self.getfilefromlink(file_path)
                else:
                    file_path = self.links[file_path]

        if self.files[file_path]['permission'] not in ['w','rw']:
            return False
        if self.quota < len(content):
            return False
        
        self.files[file_path]['content'] =content
        return True
    
    def mkdir(self,path:str)->bool:
        

        parent,_,cur = path.rpartition('/')

        

        if parent not in self.directory:
            return False
        self.directory[path] = {'parent':parent,'name':cur}

        return True



    def mkdir_p(self,dir_path:str)->bool:

        parent,_,cur = dir_path.rpartition('/')

        dir_list =copy.deepcopy(self.directory)

        if parent not in dir_list:
            self.mkdir_p(parent)
        self.directory[dir_path] = {'parent':parent,'name':cur}

        return True
        
    
    def ls(self,dir:str)->list:
        lst =[]

        for f in self.files:
            if dir in f and dir !=f:

                _,_,name = f.rpartition('/')
                lst.append(name)

        for f in self.directory:
            if dir in f and dir !=f:

                _,_,name = f.rpartition('/')
                lst.append(name)

        if lst == []:
            return None

        return lst
    def delete_recursive(self,dir:str)->bool:
        
        delfiles =[]
        for f in self.files:
            if dir in f:
                delfiles.append(f)
        for x in delfiles:
            del self.files[x]
        delfiles =[]

        for f in self.directory:
            if dir in f:
                delfiles.append(f)
        for x in delfiles:
            del self.directory[x]

        return True


        
    
 
    
    def exists(self,filename:str)->bool:

       
        if filename in self.files:
            return True
        
        if filename in self.directory:
            return True
        
        return False
    
    def is_file(self,filename:str)->bool:

        
       
        if filename in self.files:
            return True
        return False
        
        return False
    def is_directory(self,dirname:str) ->bool:
        
        if dirname in self.directory:
            return True
        return False
    def move(self,source:str,dest:str)->bool:

        if source not in self.files and source not in self.directory:
            return False

        # Moving a file
        if source in self.files:
            self.create_file(dest,self.files[source]['content'])
            del self.files[source]
            return True

        # Moving a directory — check for move-into-self
        if dest.startswith(source + "/"):
            return False

        # Move all files under source
        files_to_move = [f for f in self.files if f == source or f.startswith(source + "/")]
        for f in files_to_move:
            new_path = dest + f[len(source):]
            self.files[new_path] = self.files[f]
            del self.files[f]

        # Move all directories under source (including source itself)
        dirs_to_move = [d for d in self.directory if d == source or d.startswith(source + "/")]
        for d in dirs_to_move:
            new_path = dest + d[len(source):]
            self.directory[new_path] = self.directory[d]
            del self.directory[d]

        return True
    def copy(self,source:str,dest:str)->bool:
       count=0
       if dest.startswith(source + "/"):
            return False

       if source in self.files:
        if  len(self.files[source]['content'])*2 > self.quota:
            return False

        return self.create_file(dest,self.files[source]['content'])
       
       copylist = [f for f in self.files if f.startswith(source)]
       for f in copylist:
            count += len(self.files[f]['content'])
       if count*2 > self.quota:
           return False 
       for f in copylist:
            new_path = dest + f[len(source):]
            self.files[new_path] = self.files[f]
           

       dirlist = [d for d in self.directory if d.startswith(source)]

       for d in dirlist:
           new_path = dest+ d[len(source):]
           self.directory[new_path] = self.directory[d]

       return True
    
    def find (self,start:str,end:str)->list:

        lst = [x for x in self.files if x.startswith(start)and x.endswith(end)]

        return lst
    def grep(self,dest:str,cont:str) ->list:

        filelist = [x for x in self.files if cont in self.files[x]['content'] and x.startswith(dest) ]

        return filelist
        
    def get_size(self,filename:str)->int:

        if filename in self.files:

            return len(self.files[filename]['content'])
        else:

            count =0
            for x in self.files:
                if x.startswith(filename):
                    count += len(self.files[x]['content'])
            return count
    def disk_usage(self)->int:
        count=0
        for x in self.files:
            count += len(self.files[x]['content'])
        return count
    def set_quota(self,quota:int)->bool:
        self.quota = quota
        return True
    
    def chmod(self,filename:str, permission:str)->bool:

        self.files[filename]['permission'] = permission
        return  True
    
    def symlink(self,source:str,dest:str)->bool:

        self.links[dest] = source

        return True



