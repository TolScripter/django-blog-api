##Description => Django Blog API

####Fonctionnalités: 
* Authentification basé sur le Json Web Token (JWT)
* CRUD pour les articles
* Like - Vue - Collection (Favoris)

####Prochaines fonctionnalités: 
* Authentification Google
* Validation OTP pour les inscriptions
* Ajout de système d'affiliation 
** Système de recommandation d'articles basé sur l'IA

####Points de terminaison (Endpoints / Routes)

#users routes
- POST 'user/register/' {username, email, password, is_superuser:[Boolean]} => Registration
- POST 'user/login/' {email, password} => User Login
- GET/DELETE/PUT 'user/details/<int:id>', Read/Delete/Update User account (Authentification Required)

#tags routes
- POST/GET 'blog/tags/' {title, code, description} => Create New Tag OR Get All Tags
- GET/DELETE/PUT' blog/tag/details/<int:id>' => Read/Delete/Update Tag details (Authentification Required)

#categories routes
- POST/GET 'blog/categories/'
- GET/DELETE/PUT 'blog/category/details/<int:id>'

#posts routes
- POST/GET 'blog/posts/'
- GET/DELETE/PUT 'blog/post/details/<int:id>'

#likes routes
- POST/GET 'post/likes/'
- GET/DELETE/PUT 'post/like/details/<int:id>'

#views routes
- POST/GET 'post/views/' 

#collections routes
<<<<<<< HEAD
- POST/GET 'post/collections/'
- GET/DELETE/PUT 'post/collection/details/<int:id>'
=======
- POST/GET 'post/collection/'
- GET/DELETE/PUT 'post/collection/details/<int:id>'
>>>>>>> b72c0c978029aa80d8f454c8c0125e3318f7756b
