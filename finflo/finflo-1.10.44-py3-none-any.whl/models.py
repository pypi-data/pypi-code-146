# sourcery skip: raise-specific-error
from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import models
from .base_enum import Values
from .exception import ModelError
from .middleware import get_current_user
from .validators import validate_postive

try:
   from django.conf import settings
except ImportError as e:
   raise Exception("settings.py file is required to run this package") from e
from django.conf import settings


## CORE CONFIGURATIONS CLASSES ##


class Flowmodel(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['id']
        verbose_name_plural = "1. Flowmodel"



class Party(models.Model):
    description = models.CharField(max_length=255 , unique = True)

    def __str__(self):
        return self.description

    class Meta:
        ordering = ['id']
        verbose_name_plural = "2. Party"


class TransitionManager(models.Model):
    t_id = models.IntegerField()
    type = models.CharField(max_length = 255 )
    sub_sign = models.IntegerField(default = 0 , editable = False)
    in_progress = models.BooleanField(default = False)
    created_date = models.DateTimeField(auto_now_add=True)
    
    # default 1 for initial submit and NO_SIGN process
    
    def __str__(self):
        return "{0}_{1}".format(self.type.capitalize() , self.t_id)
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = "4. TransitionManager"


class SignList(models.Model):
    sign_id = models.IntegerField(validators=[validate_postive],editable = False,blank=True, null=True)
    name = models.CharField(max_length = 255 , unique = True )
    sub_action_name = models.CharField(max_length = 255 , unique = True)

    def __str__(self):
        return self.name
     
    class Meta:
        ordering = ['id']
        verbose_name_plural = "5. Signatures"

    def save(self,*args, **kwargs):
       super(SignList, self).save(*args, **kwargs)
       sign_list_counter = SignList.objects.all().count()
       for i in range(sign_list_counter):
          SignList.objects.filter(id = i+1).update(sign_id = i)
       return None
    



def party_models():
    try: 
        return settings.FINFLO['PARTY_MODEL'][0] or Party
    except Exception:
        return Party
    

class States(models.Model):
    description = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['id']
        verbose_name_plural = "6. States"

    def __str__(self): 
        return self.description
    
    def save(self, *args, **kwargs):
        self.description = self.description.capitalize()
        return super(States, self).save(*args, **kwargs) 


class Action(models.Model):
    party = models.ForeignKey(party_models() , models.CASCADE , blank = True , null = True , help_text = 'this field is optional' , related_name = 'party_model')
    description = models.CharField(max_length=255 , blank = True , null=True , help_text = 'e.g., SUBMIT , DELETE') 
    model = models.ForeignKey(Flowmodel , on_delete = models.CASCADE , blank = True , null = True )
    from_state = models.ForeignKey(States , on_delete= models.DO_NOTHING , related_name = 'action_from_state' , blank = True , null = True , help_text = "initial from state for transition ")
    to_state = models.ForeignKey(States , on_delete= models.DO_NOTHING , blank = True , null = True , help_text = "final state for the transition to take place")
    intermediator = models.BooleanField(default = False)
    from_party = models.ForeignKey(party_models() , models.CASCADE , blank = True , null = True , help_text = 'this field is optional' , related_name = 'from_transition_party_type')
    to_party = models.ForeignKey(party_models() , models.CASCADE , blank = True , null = True , help_text = 'this field is optional' , related_name = 'to_transition_party_type')
    stage_required = models.ForeignKey(SignList , on_delete= models.DO_NOTHING ,blank = True , null = True ,help_text = "this field is optional , IMPORTANT : if NO_SIGN means initial_transition")
    sign_required = models.IntegerField(default=0,editable = False,help_text = "IMPORTANT : if 0 means initial_transition " , blank=True, null=True )

 
    def save(self, *args, **kwargs):
        self.description = self.description.upper()
        try:
            sign_len = SignList.objects.get(name = self.stage_required.name )
            self.sign_required = sign_len.sign_id
        except Exception:
            self.sign_required = 0
        return super(Action,self).save(*args, **kwargs)

    
    
    def __str__(self):
        return self.description

    class Meta:
        ordering = ['id']
        verbose_name_plural = "3. Action"
        unique_together = ('description', 'model' ) 
 

class workflowitems(models.Model):
    
    created_date = models.DateTimeField(auto_now_add=True)
    transitionmanager = models.OneToOneField(TransitionManager, on_delete=models.CASCADE,blank=True, null=True )
    initial_state  = models.CharField(max_length=50,default = Values.DRAFT.value)
    interim_state = models.CharField(max_length=50,default = Values.DRAFT.value)
    final_state = models.CharField(max_length=50,default = Values.DRAFT.value) 
    event_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL , blank=True, null=True)
    next_available_transitions =  models.JSONField(blank=True, null=True)
    current_from_party = models.CharField(max_length = 500  , blank = True , null = True )
    current_to_party = models.CharField(max_length =  500 ,  blank = True , null = True )
    action = models.CharField(max_length=25 , blank=True, null=True , default = Values.DRAFT.value)
    subaction = models.CharField(max_length=55 , blank=True, null=True)
    previous_action = models.CharField(max_length=55 , blank=True, null=True)
    record_datas = models.JSONField(blank=True, null=True)
    model_type  = models.CharField(max_length=55, blank=True, null=True)
    comments = models.CharField(max_length=500,blank=True, null=True)
    is_read = models.BooleanField(default=True,blank=True, null=True)
    final_value = models.BooleanField(default=False,blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "7. WorkFlowItem"
        ordering = ['id']
    
    



# WORKEVENTS
class workevents(models.Model):

    workflowitems = models.ForeignKey(workflowitems, on_delete=models.CASCADE , related_name='WorkFlowEvents')
    action = models.CharField(max_length=25, blank=True, null=True , default = Values.DRAFT.value)
    subaction = models.CharField(max_length=55 , blank=True, null=True , default = Values.DRAFT.value)
    initial_state  = models.CharField(max_length=50 , default = Values.DRAFT.value)
    interim_state = models.CharField(max_length=50,default = Values.DRAFT.value)
    final_state = models.CharField(max_length=50,default = Values.DRAFT.value)
    from_party = models.CharField(max_length = 500  , blank = True , null = True )
    to_party = models.CharField(max_length = 500  , blank = True , null = True )
    event_user = models.ForeignKey(settings.AUTH_USER_MODEL,  on_delete=models.SET_NULL , blank=True, null=True)
    is_read = models.BooleanField(default=True,blank=True, null=True)
    record_datas = models.JSONField(blank=True, null=True)
    final_value = models.BooleanField(default=False,blank=True, null=True)
    comments = models.CharField(max_length=500,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=55, blank=True, null=True)
    
    
    class Meta:
        verbose_name_plural = "8. WorkFlowEvent"
        ordering = ['id']



    
        





