class Project(models.Model):
    """
    A client is a TechGenies customer, typically someone with a development team and a product
    """
    name = models.CharField(max_length=100, help_text='The name of this project')
    # logo = models.FileField(blank=True, null=True, upload_to=client_logo_path, validators=[FileExtensionValidator(extensions=['jpg', 'png'])])
    notifications_enabled = models.BooleanField(default=True, help_text='Deliver email/sms notifications to users associated with this project')
    inactive = models.BooleanField(default=False, help_text='Mark old projects inactive to keep data w/out deleting')
    description = models.CharField(max_length=400, help_text='snippet of info about project')
    #time_elapsed
    #date_created
    #
    
    # TODO 
    # team_profiles = models.ManyToManyField(TeamProfile, blank=True, help_text='The developers or resources for this client')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    @staticmethod
    def get_serializer():
        return import_string('project.serializers.ProjectSerializer')