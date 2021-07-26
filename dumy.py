
# ------------ create records ---------------

from polls.models import Blog, Post, Author
b = Blog(name='Sport Blog', description='All the latest sport news.')
b.save()

b.name = 'Football Blog'
b.description = 'All the latest football news.'
b.save()

p = Post()
p.title = 'Messi'
p.description = 'Messi'
p.number_of_likes = 67
p.blog = b
p.save()

mohammad = Author(name='Mohammad')
mohammad.save()
zahra = Author.objects.create(name="Zahra")

p.authors.add(mohammad, zahra)


# create 2 other blog
# create 3 new user
# create 2 post in each blog
# assign some user to these blogs

from django.utils import timezone
p = Post()
p.title = 'Ronaldo would transfer this year'
p.description = 'There are some rumours around Ronaldo that he would transfer to PSG this year'
p.number_of_comments = 200
p.number_of_likes = 56
p.blog = Blog.objects.get(name='Football Blog')
p.save()
Post.objects.filter(pk=p.pk).update(
    pub_date=timezone.datetime(year=2020, month=10, day=20).date(),
    mod_date=timezone.datetime(year=2021, month=1, day=9).date()
)
p.authors.add(mohammad)

p = Post()
p.title = 'Neymar is not happy in PSG'
p.description = 'In last game, there was a fight between Neymar and his teammate'
p.pub_date = timezone.datetime(year=2021, month=10, day=20).date()
p.mod_date = timezone.datetime(year=2021, month=6, day=1).date()
p.number_of_comments = 0
p.number_of_likes = 0
p.blog = Blog.objects.get(name='Football Blog')
p.save()
Post.objects.filter(pk=p.pk).update(
    pub_date=timezone.datetime(year=2021, month=10, day=20).date(),
    mod_date=timezone.datetime(year=2021, month=6, day=1).date()
)

ali = Author.objects.create(name="Ali")
reza = Author.objects.create(name="Reza")
morteza = Author.objects.create(name='Morteza')

b = Blog(name='Game Blog', description='News about upcoming games and game plays')
b.save()

p = Post()
p.title = 'Games that we are waiting for in 2022'
p.description = 'Here is list of game which would release in 2022'
p.number_of_comments = 10
p.number_of_likes = 32
p.blog = b
p.save()
Post.objects.filter(pk=p.pk).update(
    pub_date=timezone.datetime(year=2021, month=6, day=20).date(),
    mod_date=timezone.datetime(year=2021, month=6, day=1).date()
)
p.authors.add(ali)

p = Post()
p.title = 'Is cyberpunk 2077 dead?'
p.number_of_comments = 50
p.number_of_likes = 43
p.blog = b
p.save()
Post.objects.filter(pk=p.pk).update(
    pub_date=timezone.datetime(year=2021, month=6, day=20).date(),
    mod_date=timezone.datetime(year=2021, month=6, day=1).date()
)
p.authors.add(ali, morteza)


b = Blog(name='Movie', description='We Talk about movies and stuff here')
b.save()

p = Post()
p.title = 'Have you seen Titanic?'
p.number_of_comments = 100
p.number_of_likes = 5
p.blog = b
p.save()
p.authors.add(reza)

p = Post()
p.title = 'Is Inception worth seeing?'
p.description = 'Inception is one of nolan movies which got very high score in IMDB'
p.number_of_comments = 23
p.number_of_likes = 67
p.blog = b
p.save()
p.authors.add(reza)

# ------------ retrieving ---------------



