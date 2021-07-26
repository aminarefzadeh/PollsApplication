
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


# ------------ retrieving ---------------

# retrieving all objects

query_set = Post.objects.all()

for post in query_set:
    print(post.title)

post = query_set[0]
post = query_set[-1]

len(query_set)

# filter

# simple filter
query_set = Post.objects.filter(number_of_comments=0)

# exclude
query_set = Post.objects.exclude(number_of_comments=0)

# chaining
query_set = Post.objects.filter(number_of_comments=0, number_of_likes=0)

query_set = Post.objects.filter(number_of_comments=0)
query_set = query_set.filter(number_of_likes=0)

query_set = Post.objects.filter(number_of_comments=0).exclude(number_of_likes=0)

# gt, gte, lt, lte
query_set = Post.objects.filter(number_of_likes__gte=50)
from django.utils import timezone
query_set = Post.objects.filter(pub_date__gt=timezone.now().date())

# year, month, day
query_set = Post.objects.filter(pub_date__year=2021, pub_date__month=6)
query_set = Post.objects.filter(pub_date__year=2021, pub_date__month__gt=6)

# startswith, contain, endswith
Post.objects.filter(title__startswith='Is')

Post.objects.filter(title__contains='20')

Post.objects.filter(title__endswith='?')

# in
Post.objects.filter(pub_date__month__in=[6, 10])

# order_by
Post.objects.exclude(number_of_comments=0).order_by('number_of_likes')
Post.objects.exclude(number_of_comments=0).order_by('-number_of_likes')

Post.objects.order_by('-number_of_likes', '-number_of_comments')


# limiting

Post.objects.order_by('-number_of_likes')[:5]   # limit 5

Post.objects.order_by('-number_of_likes')[5:10]   # offset 5 limit 5


# get

b = Blog.objects.get(name='Football Blog')
b.id
b.name
b.description

# raises exception when 0 or more than 1 record found
b = Blog.objects.get(name='Football')

p = Post.objects.filter(number_of_likes=67)


# relation lookup

Post.objects.filter(blog__name='Football Blog')
Post.objects.filter(blog__in=Blog.objects.filter(id__lt=3))
Post.objects.filter(blog_id__in=[1, 2])

Post.objects.filter(authors__in=[Author.objects.get(name='Zahra'), Author.objects.get(name='Mohammad')])
Post.objects.filter(authors__in=[Author.objects.get(name='Zahra'), Author.objects.get(name='Mohammad')]).distinct()


Blog.objects.filter(post__authors__name='Ali')
Blog.objects.filter(post__authors__name='Ali').distinct()


# relational fields in model --> remove, clear, set

post = Post.objects.get(title='Messi')
post.blog
post.blog_id

post.authors
post.authors.all()
post.authors.filter(name__contains='M')

# add function
reza = Author.objects.get(name="Reza")
post.authors.add(reza)
post.authors.all()

# remove function
post.authors.remove(reza)
post.authors.all()

# set function
mohammad = Author.objects.get(name='Mohammad')
post.authors.set([mohammad, reza])
post.authors.all()

# clear function
post.authors.clear()
post.authors.all()

# create function
majid = post.authors.create(name='Majid')
post.authors.all()

# reverse

blog = Blog.objects.get(name='Football Blog')
blog.post_set.all()

author = Author.objects.get(name='Mohammad')
author.post_set.all()
# can change post_set field to what ever with 'related_name' param

# F
from django.db.models import F
Post.objects.filter(number_of_comments__gt=F('number_of_likes') * 2)
Post.objects.all().order_by(-1 * (F('number_of_likes') + F('number_of_comments') + 2))

# or with Q
from django.db.models import Q
Post.objects.filter(Q(number_of_likes__gt=50) | ~Q(number_of_comments__lte=50))

query1 = Q(number_of_likes__gt=50)
query2 = Q(number_of_comments__gt=50)
query = query1 & query2
Post.objects.filter(query)

# annotate (yekam advance nagim benazaram)

# aggregate (advance)

# values --> just fetch limited fields for better performance (not select *)
Post.objects.values('id', 'description', 'blog__name')

# caching
# QuerySets are lazy. not performing query until evaluation. you can stack too many filters without actually running query

from datetime import date
q = Post.objects.filter(blog__name="Football Blog")     # doesn't hit database
q = q.filter(pub_date__lte=date.today())    # doesn't hit database
q = q.exclude(description__contains="is")   # doesn't hit database
print(q)    # hits database

# first time a query_set evaluated it stores its results in memory cache for future evaluation

print([e.headline for e in Post.objects.all()])     # hits database
print([e.pub_date for e in Post.objects.all()])     # hits database again


queryset = Post.objects.all()   # doesn't hit database
print([p.headline for p in queryset])   # hits database and caches its results
print([p.pub_date for p in queryset])   # doesn't hit database, use its cache


# get single element won't populate the cache
queryset = Post.objects.all()
print(queryset[5]) # hits the database
print(queryset[5]) # hits the database again

queryset = Post.objects.all()
[entry for entry in queryset]   # Queries the database and populate its cache
print(queryset[5]) # Uses cache
print(queryset[5]) # Uses cache

# for relational fields cache won't populated at first.
post = Post.objects.get(title='Messi')  # retrieve post from db
post.blog.name  # retrieving blog from db
post.blog.name  # use cache

# you can use select_related to prefetch one-to-many (foreign-key) relations and store them in cache ahead of time
post = Post.objects.select_related().get(title='Messi')     # retrieve post and blog from db
post.blog.name  # use cache
post.blog.name  # use cache


# compare two record
post1 = Post.objects.get(title='Messi')
post2 = Post.objects.get(title='Messi')

post1 == post2 # returns True. this is equivalent to post1.pk == post2.pk
post1 is post2 # returns False. don't use this


# update multiple
Post.objects.filter(blog__name='Football Blog').update(number_of_likes=10)

# delete
post = Post.objects.get(title='Messi')
post.delete()

query_set = Post.objects.filter(blog__name='Football Blog')
query_set.delete()


# یه سوال
# ازشون بخوایم یه پست رو از دیتابیس بگیرن با get
# و تعداد لایک هاش رو یه دونه اضافه کنن و بعد هم save کنن

# this code has race condition
post = Post.objects.get(title='Have you seen Titanic?')
post.number_of_likes += 1
post.save()

# should replaced by this code
post = Post.objects.get(title='Have you seen Titanic?')
post.number_of_likes = F('number_of_likes') + 1
post.save()



