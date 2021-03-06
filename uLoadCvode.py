
import ctypes as ct, os
import numpy as np

CV_BDF = 2
CV_ADAMS = 1
CV_NORMAL = 1
CV_SUCCESS = 0

def setUserData (n):
       return ct.c_double * n
    
PARAMETER_ARRAY = setUserData (2)

class cvodeuserdata (ct.Structure):
      _fields_ = [('k', PARAMETER_ARRAY)]
      
      
# The ode function has the form f(t, y, ydot, user_data)
callback_type = ct.CFUNCTYPE(ct.c_int, ct.c_double, ct.c_void_p, ct.c_void_p, ct.c_void_p)
error_callback_type = ct.CFUNCTYPE(None, ct.c_int, ct.c_char_p, ct.c_char_p, ct.c_char_p, ct.c_void_p)
Jac_callback_type = ct.CFUNCTYPE(ct.c_int, ct.c_double, ct.c_void_p, ct.c_void_p,
                    ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p, ct.c_void_p)

#int (*CVLsJacFn)(realtype t, N Vector y, N Vector fy,
#SUNMatrix Jac, void *user data,
#N Vector tmp1, N Vector tmp2, N Vector tmp3);

# if os.path.exists("sundials_cvode.dll"):
#    dllcvode = ct.WinDLL ("sundials_cvode.dll")
# else:
#    print ("Cannot find cvode dll")   

# if os.path.exists("sundials_nvecserial.dll"):
#    dllnvector = ct.WinDLL ("sundials_nvecserial.dll")
# else:
#    print ("Cannot find nvecserial dll") 
   
# dllcvode.CVodeCreate.restype = ct.c_void_p
# dllcvode.CVodeCreate.argTypes = [ct.c_int]

# dllcvode.CVodeSetMinStep.argTypes = [ct.c_void_p, ct.c_double]
# dllcvode.CVodeSetMinStep.restype = ct.c_longlong

# dllcvode.CVodeSetUserData.argTypes = [ct.c_void_p, ct.c_void_p]

# dllnvector.N_VGetArrayPointer_Serial.argTypes = [ct.c_void_p]
# dllnvector.N_VGetArrayPointer_Serial.restype = ct.POINTER(ct.c_double)

# dllnvector.N_VNew_Serial.restype = ct.c_void_p
# dllnvector.N_VNew_Serial.argTypes = [ct.c_longlong]

# dllcvode.CVodeSStolerances.restype = ct.c_int
# dllcvode.CVodeSStolerances.argTypes = [ct.c_void_p, ct.c_double, ct.c_void_p]

# dllcvode.SUNDenseMatrix.restype = ct.c_void_p
# dllcvode.SUNDenseMatrix.argTypes = [ct.c_int, ct.c_int]

# dllcvode.SUNLinSol_Dense.restype = ct.c_void_p
# dllcvode.SUNLinSol_Dense.argTypes = [ct.c_void_p,  ct.c_void_p]

# dllcvode.CVodeSetLinearSolver.restype = ct.c_int
# dllcvode.CVodeSetLinearSolver.argTypes = [ct.c_void_p, ct.c_void_p,ct.c_void_p, ]
  
# dllcvode.CVode.restype = ct.c_int
# dllcvode.CVode.argTypes = [ct.c_void_p, ct.c_double, 
#           ct.c_void_p, ct.POINTER(ct.c_double), ct.c_int64]  

class TCvode:
    
    def __init__(self, algType=CV_BDF, ignoreErrors=True):
      self.ignoreErrors = ignoreErrors
      self.cvode_mem = None
      self.dllcvode = None
      self.dllnvector = None
      if os.path.exists(".\\cvode\\sundials_cvode.dll"):
         self.dllcvode = ct.WinDLL (".\\cvode\\sundials_cvode.dll")
      else:
         print ("Cannot find cvode dll")   

      if os.path.exists(".\\cvode\\sundials_nvecserial.dll"):
         self.dllnvector = ct.WinDLL (".\\cvode\\sundials_nvecserial.dll")
      else:
         print ("Cannot find nvecserial dll")  
 
      self.dllcvode.CVodeCreate.restype = ct.c_void_p
      self.dllcvode.CVodeCreate.argTypes = [ct.c_int]

      self.dllcvode.CVodeInit.restype = ct.c_int
      self.dllcvode.CVodeInit.argType = [ct.c_void_p, callback_type, ct.c_double, ct.c_void_p]
      
      self.dllcvode.CVodeSetMinStep.argTypes = [ct.c_void_p, ct.c_double]
      self.dllcvode.CVodeSetMinStep.restype = ct.c_longlong
    
      self.dllcvode.CVodeSetUserData.argTypes = [ct.c_void_p, ct.c_void_p]
    
      self.dllnvector.N_VGetArrayPointer_Serial.argTypes = [ct.c_void_p]
      self.dllnvector.N_VGetArrayPointer_Serial.restype = ct.POINTER(ct.c_double)
    
      self.dllnvector.N_VNew_Serial.restype = ct.c_void_p
      self.dllnvector.N_VNew_Serial.argTypes = [ct.c_longlong]
    
      self.dllcvode.CVodeSStolerances.restype = ct.c_int
      self.dllcvode.CVodeSStolerances.argTypes = [ct.c_void_p, ct.c_double, ct.c_void_p]
    
      self.dllcvode.SUNDenseMatrix.restype = ct.c_void_p
      self.dllcvode.SUNDenseMatrix.argTypes = [ct.c_int, ct.c_int]
    
      self.dllcvode.SUNLinSol_Dense.restype = ct.c_void_p
      self.dllcvode.SUNLinSol_Dense.argTypes = [ct.c_void_p, ct.c_void_p]

      self.dllcvode.CVodeSetLinearSolver.restype = ct.c_int
      self.dllcvode.CVodeSetLinearSolver.argTypes = [ct.c_void_p, ct.c_void_p, ct.c_void_p]
      
      self.dllcvode.CVode.restype = ct.c_int
      self.dllcvode.CVode.argTypes = [ct.c_void_p, ct.c_double, 
              ct.c_void_p, ct.POINTER(ct.c_double), ct.c_int64] 
           
      self.dllcvode.CVodeSetErrHandlerFn.restype = ct.c_int
      self.dllcvode.CVodeSetErrHandlerFn.argType = [ct.c_void_p, error_callback_type, ct.c_void_p]
      
      self.cvode_mem = ct.c_void_p(self.dllcvode.CVodeCreate (algType))
      
    def setIgnoreErrors (ignoreErrors):
        self.ignoreErrors = ignoreErrors
        
    def errorHandler (self, errorCode, module, function, msg, eg_data):
        if not self.ignoreErrors: 
           print ("Bad model ----------- " + str (errorCode), end = '')
        #print (function)
        #print (msg)
        
    def setModel (self, fcn, JacFcn=None):
        self.fcn = fcn
        if JacFcn != None:
           self.JacFcn = fcn
           self.Jac_callback_func = Jac_callback_type (fcn)
        else:
           self.JacFcn = None
           
        self.callback_func = callback_type (fcn)
        self.error_callback_func = error_callback_type (self.errorHandler)
        self.dllcvode.CVodeSetErrHandlerFn (self.cvode_mem, self.error_callback_func, None)
        
    def setVectorValue (self, v, index, value):
        py = self.dllnvector.N_VGetArrayPointer_Serial (ct.c_void_p (v))
        py[index] = value
        
    def getVectorValue (self, v, index):
        py = self.dllnvector.N_VGetArrayPointer_Serial (ct.c_void_p (v))
        return py[index]
    
    def getVectorArray (self, v):
        return self.dllnvector.N_VGetArrayPointer_Serial (ct.c_void_p (v))
       
    def setTolerances (self, reltol=1E-6, abstol=1E-16):
        _abstol = self.dllnvector.N_VNew_Serial (self.NEQ)
        pabstol = self.dllnvector.N_VGetArrayPointer_Serial (ct.c_void_p (_abstol))
        for i in range (self.NEQ):
            pabstol[i] = abstol

        self.dllcvode.CVodeSStolerances (self.cvode_mem, ct.c_double (reltol), ct.c_void_p (_abstol))

    def initialize (self, n, y0, userData=None):
        self.NEQ = n
        self.init_y0 = self.dllnvector.N_VNew_Serial (self.NEQ)
        self.init_y0_ptr = self.dllnvector.N_VGetArrayPointer_Serial (ct.c_void_p (self.init_y0))
        for i in range (self.NEQ):
            self.init_y0_ptr[i] = y0[i]        
        
        flag = self.dllcvode.CVodeSetUserData (self.cvode_mem, None)
        t0 = ct.c_double (0.0)
        flag = self.dllcvode.CVodeInit (self.cvode_mem, self.callback_func, t0, ct.c_void_p (self.init_y0))
        if flag != 0:
           print ("Error in calling CVodeInit: ", flag)

         # Create dense SUNMatrix for use in linear solves 
        A = self.dllcvode.SUNDenseMatrix(self.NEQ, self.NEQ)
        #  if(check_retval((void *)A, "SUNDenseMatrix", 0)) return(1)

        # Create dense SUNLinearSolver object for use by CVode 
        LS = self.dllcvode.SUNLinSol_Dense(ct.c_void_p (self.init_y0), ct.c_void_p (A))
        #  if(check_retval((void *)LS, "SUNLinSol_Dense", 0)) return(1);

        # Call CVodeSetLinearSolver to attach the matrix and linear solver to CVode 
        flag = self.dllcvode.CVodeSetLinearSolver(self.cvode_mem, ct.c_void_p (LS), ct.c_void_p (A))
       
        if self.JacFcn != None:
           flag = self.dllcvode.CVodeSetJacFn(self.cvode_mem, JacFcn)
        
        self.setTolerances ()
        
    def reset ():
        t0 = ct.c_double (0.0)
        flag = self.dllcvode.CVodeInit (self.cvode_mem, self.callback_func, t0, ct.c_void_p (self.init_y0))
 
    def oneStep (self, t, hstep):
        new_t = ct.c_double (0)
        tout =  ct.c_double (t + hstep)
        print ("tout = ", tout.value)
        yout = self.dllnvector.N_VNew_Serial (self.NEQ)
        print ("neq = ", self.NEQ)
        ier = self.dllcvode.CVode (self.cvode_mem, tout, 
                      ct.c_void_p (yout), 
                      ct.byref(new_t), CV_NORMAL)
        print ("ier = ", ier)

        py = self.dllnvector.N_VGetArrayPointer_Serial (ct.c_void_p (yout))
        print("Ans = ", new_t.value, py[0])
        y = []
        for i in range (self.NEQ):
            y.append (py[i])
        return t + hstep, y
    
    def simulate (self, startTime, endTime, numPoints):
        yreturn = np.zeros ([numPoints, self.NEQ+1])  # plus one for time
        yreturn[0,0] = startTime
        for i in range (self.NEQ):
            yreturn[0, i+1] = self.init_y0_ptr[i]
            
        hstep = (endTime - startTime)/(numPoints-1)
        new_t = ct.c_double (0)
        yout = self.dllnvector.N_VNew_Serial (self.NEQ)
        tout =  ct.c_double (startTime + hstep)
   
        for i in range (numPoints-1):
          ier = self.dllcvode.CVode (self.cvode_mem, tout, 
                        ct.c_void_p (yout), 
                        ct.byref(new_t), CV_NORMAL)
          if ier < 0:
              raise Exception("Error: " + str (ier))
              
          py = self.dllnvector.N_VGetArrayPointer_Serial (ct.c_void_p (yout))
          # +1 because time = 0 is stored at i=0
          yreturn[i+1, 0] = new_t.value
          for j in range (self.NEQ):
              yreturn[i+1, j+1] = py[j]
          tout.value = tout.value + hstep
        return yreturn
   
#new_t = ct.c_double (0)
#tout =  ct.c_double (1)
#yout = dllnvector.N_VNew_Serial (NEQ)
   
##for i in range (15):
#   ier = dllcvode.CVode (cvode_mem, tout, 
#                      ct.c_void_p (yout), 
#                      ct.byref(new_t), CV_NORMAL)
   #print ("ier = ", ier)

   

