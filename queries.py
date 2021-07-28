
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
post = query_set[-1]       #exception

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


# tamrin

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


# tamrin:
# تابعی بنویسید که یک string ورودی بگیره و پست هایی رو برگردونه که مال حداکثر ۱ ماه پیش هستند و اون string رو داخل تایتل شون دارن
# پست هایی امروز رو پیدا کنید که تعداد لایک هاشون بیشتر از ۱۰ تا باشه
# تایتل های پست هایی که امروز پابلیش شدن رو پرینت کنید.
# تعداد پست هایی که تایتلشون با ? تموم شده و تعداد کامنت هاشون بین ۵۰ و ۱۰۰ هست رو پیدا کنید
# پستهایی که تعداد کامنتشون زیر ۱۰۰ و تعداد لایک شون بالای ۵۰ هست رو فقط با استفاده از exclude پیدا کنید
# javab:  Post.objects.exclude(number_of_comments__gte=100).exclude(number_of_likes__lte=50)
# تمام پستهایی رو پیدا کنید که تعداد کامنت هاشون زیر ۱۰۰ عه یا تعداد لایک هاشون بالای ۵۰ عه
# javab: Post.objects.exclude(number_of_comments__gte=100, number_of_likes__lte=50)
# توضیح بدیم در مورد این دو تا سوال بالا
# یدونه پست پیدا کنید که هم داخل دیسکریپشن و هم داخل تایتلش ؟ باشه
# یه تابع بنویسید با ۳ تا ورودی بولین. new و question و hot. نیو پست های ۱ ماه اخیر میشه. question پست هایی که توی تایتلشون ؟ باشه و هات پست هایی که تعداد لایک هاشون بیشتر از ۵۰ باشه


# order_by
Post.objects.exclude(number_of_comments=0).order_by('number_of_likes')
Post.objects.exclude(number_of_comments=0).order_by('-number_of_likes')

Post.objects.order_by('-number_of_likes', '-number_of_comments')


# limiting

Post.objects.order_by('-number_of_likes')[:5]   # limit 5

Post.objects.order_by('-number_of_likes')[5:10]   # offset 5 limit 5


# tamrin:
# آیدی ۵ تا از پر کامنت ترین پست های امروز رو پیدا کنید.
# پستی که از همه کمتر لایک داشته رو پیدا کنید
# پست ها رو بر اساس لایک به ترتیب نزولی و بر اساس کامنت به ترتیب صعودی سورت کنید

# get

b = Blog.objects.get(name='Football Blog')
b.id
b.name
b.description

# raises exception when 0 or more than 1 record found
b = Blog.objects.get(name='Football')

p = Post.objects.get(number_of_likes=67)


# relation lookup

Post.objects.filter(blog__name='Football Blog')
Post.objects.filter(blog__in=Blog.objects.filter(id__lt=3))
Post.objects.filter(blog_id__in=[1, 2])

Post.objects.filter(authors__in=[Author.objects.get(name='Zahra'), Author.objects.get(name='Mohammad')])
Post.objects.filter(authors__in=[Author.objects.get(name='Zahra'), Author.objects.get(name='Mohammad')]).distinct()


# tamrin:
# تمام پست هایی که یوزری با اسم Mohammad گذاشته رو پیدا کنید.
# یه تابع بنویسید که لیست از آیدی کاربرها رو بگیره و به ازای هر کاربر پر لایک ترین پستش رو برگردونه
# یه تابع بنویسید که لیستی از کاربرها بگیره و ۱۰ تا پستی پر لایکی که یکی از اون کاربرها حداقل نویسنده اش بوده رو برگردونه
# javab: Post.objects.filter(authors__in=author_list).distinct().order_by('-number_of_likes')[:10]
# بلاگ هایی رو پیدا کنید که یوزر های با آیدی ۱ و ۲ توش پست گذاشته باشن
# javab: Blog.objects.filter(post__authors__id__in=[1,2]).distinct()
# بلاگ هایی رو پیدا کنید که پستی که توی تایتلش ? باشه و تعداد لایک هاش بیشتر از ۱۰ باشه نداشته باشه.
# javab: Blog.objects.exclude(
#     post__in=Post.objects.filter(
#         title__contains='?',
#         number_of_likes__gt=10,
#     ),
# )
# javab ghalat: Blog.objects.exclude(
#     post__title__contains='?',
#     post__number_of_likes__gt=10,
# )


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

# tamrin

# F
from django.db.models import F
Post.objects.filter(number_of_comments__gt=F('number_of_likes') * 2)

# tamrin:
# پست ها رو به ترتیب نزولی مجموع لایک و پست هاشون سورت کنید.
# Post.objects.all().order_by(-1 * (F('number_of_likes') + F('number_of_comments')))
# تایتل پست هایی که تایم پابلیش شدنشون بعد از تایم ادیت شدنشون هست رو پیدا کنید
# پست هایی که مجموع تعداد کامنت ها و تعداد لایکشون بیشتر از ۱۰۰ میشه رو پیدا کنید
# Post.objects.filter(number_of_likes__gt=100 - F('number_of_comments'))
# پست هایی رو پیدا کنید که توی دیسکریپشن اش اسم حداقل یکی از نویسنده هاش اومده باشه
# javab: Post.objects.filter(description__contains=F('authors__name')).distinct()

# or with Q
from django.db.models import Q
Post.objects.filter(Q(number_of_likes__gt=50) | ~Q(number_of_comments__lte=50))

query1 = Q(number_of_likes__gt=50)
query2 = Q(number_of_comments__gt=50)
query = query1 & query2
Post.objects.filter(query)

# tamrin:
# پست هایی که pub_date یا mod_date شون برای آینده است رو پیدا کنید
# پست هایی رو پیدا کنید که مجموع تعداد لایک و کامنتشون از ۵۰ بیشتر باشه یا فوتبالی باشن

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

# tamrin:
# تمام پست های مربوط به فیلم ریتینگشون برابر ۴ ست بشه
#  تمام پست های فوتبالی اگه تعداد لایک هاشون کمتر از ۱۰ بود یه دونه لایک بهشون اضافه بشه
# کل پست های مربوط به یک کاربر با آیدی ۱ رو پاک کنن

# یه سوال
# ازشون بخوایم یه پست خاص رو از دیتابیس بگیرن با get
# و تعداد لایک هاش رو یه دونه اضافه کنن و بعد هم save کنن

# this code has race condition
post = Post.objects.get(title='Have you seen Titanic?')
post.number_of_likes += 1
post.save()

# should replaced by this code
post = Post.objects.get(title='Have you seen Titanic?')
post.number_of_likes = F('number_of_likes') + 1
post.save()



