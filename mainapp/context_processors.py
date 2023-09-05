def player(request):

   return {
       'player': request.user,
   }