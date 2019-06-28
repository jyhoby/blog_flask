from flask import Blueprint, render_template, request, session, url_for, redirect
from sqlalchemy import desc
from App.models import *


blue = Blueprint('blog', __name__)

#判断登录状态的自定义函数
# def is_login():
#     username = session.get('username', '')
#     if username == '':
#         return render_template("admin/login.html")


#  登录判断的钩子函数
@blue.before_request
def islogin():
    if '/admin/' in request.path :
        if request.path == '/admin/login/':
            pass
        else:
            username = session.get('username', '')
            if username:
                pass
            else:
                return redirect(url_for('blog.admin_login'))



# 前台首页
@blue.route('/')
def index():
    blogs = Blog.query.all()
    blog_types = BlogType.query.all()
    content = {}
    content['blogs'] = blogs
    content['blog_types'] = blog_types
    return render_template('home/index.html', content=content)

# 前台博客详情
@blue.route('/blogdetail/<int:blogid>')
def blog_detail(blogid):
    blog = Blog.query.get(blogid)
    return render_template('home/blog_detail.html',blog=blog)

# 前台一种博客类型的博客列表
@blue.route('/blogtype/<int:blogtypeid>')
def blog_type_list(blogtypeid):
    blogs = Blog.query.filter_by(blog_type=blogtypeid)
    return render_template('home/blog_type_list.html',blogs=blogs)

# 前台我的相册
@blue.route('/share/')
def blog_share():
    return render_template('home/share.html')





# 后台登录
@blue.route('/admin/login/', methods=["GET", "POST"])
def admin_login():
    username = session.get('username', '')
    if username == '':
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter(User.username==username)
            for u in user:
                if u:
                    if u.password == password:
                        session['username'] = username #设置session
                        loginlog = Loginlog()
                        loginlog.username = username
                        loginlog.remote_ip = request.remote_addr
                        try:
                            db.session.add(loginlog)
                            db.session.commit()
                        except:
                            db.session.rollback()
                            db.session.flush()
                        return redirect(url_for("blog.admin_index"))
        return render_template('admin/login.html')

    return redirect(url_for('blog.admin_index'))


# 后台首页
@blue.route('/admin/index/')
def admin_index():
    username = session["username"]
    logs = Loginlog.query.order_by(desc('logintime'))
    loginnum = Loginlog.query.filter_by(username=username).count()
    adminnum = Loginlog.query.group_by('username').count()
    nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    article_num = len(Blog.query.all())

    content = {
        'username': username,
        'logs': logs,
        'loginnum': loginnum,
        'adminnum': adminnum,
        'nowtime': nowtime,
        'article_num': article_num,
    }
    return render_template('admin/index.html',content=content)


# 后台登出/注销
@blue.route('/admin/logout/')
def admin_logout():
    response = redirect(url_for('blog.admin_login'))
    session.pop('username')
    @blue.before_request
    def is_login():
        pass
    return response


# 后台文章管理页面
@blue.route('/admin/article/')
def admin_article():


    username = session['username']
    page = int(request.args.get('page', 1))  # 获取页码
    per_page = int(request.args.get('per_page', 5))  # 每页显示个数
    b = Blog.query.order_by(desc('create_time')).paginate(page, per_page, False)
    blogs = b.items
    content ={
        "blogs":blogs,
        "username":username,
        "pages":b.pages,
        "page":b.page,
        "has_next":b.has_next,
        "has_prev":b.has_prev,
        "prev_num":b.prev_num,
        "next_num":b.next_num,
    }
    return render_template("/admin/article.html",content=content)


# 后台搜索
@blue.route('/admin/search/', methods=['GET','POST'])
def admin_search():
    username = session['username']
    page = int(request.args.get('page', 1))  # 获取页码
    per_page = int(request.args.get('per_page', 5))  # 每页显示个数
    s_title = request.form.get('search')
    b = Blog.query.filter(Blog.title.contains(s_title)).paginate(page, per_page, False)
    blogs = b.items
    content ={
        "blogs":blogs,
        "username":username,
        "pages":b.pages,
        "page":b.page,
        "has_next":b.has_next,
        "has_prev":b.has_prev,
        "prev_num":b.prev_num,
        "next_num":b.next_num,
    }

    return render_template("/admin/article.html",content=content)




# 后台修改文章内容页面
@blue.route('/admin/update_article/<int:blogid>',methods=["GET","POST","DELETE"])
def admin_update_article(blogid):
    blog = Blog.query.get(blogid)
    blog_type_list = BlogType.query.all()

    if request.method == "POST":
        blog.title = request.form.get('title')
        blog.content = request.form.get('describe')
        blog.blog_type=request.form.get('category')

        try:
            db.session.commit()
            return redirect(url_for('blog.admin_article'))
        except:
            db.session.rollback()
            db.session.flush()
            return "修改失败"


    return render_template('admin/update-article.html', blog=blog,blog_type_list=blog_type_list)



# 后台添加文章页面
@blue.route('/admin/addarticle/',methods=["GET","POST"])
def admin_add_article():
    blog_type_list = BlogType.query.all()

    if request.method == "POST":
        blog = Blog()
        blog.title = request.form.get('title')
        blog.content = request.form.get('content')
        blog.blog_type = request.form.get('category')

        try:
            db.session.add(blog)
            db.session.commit()
            return redirect(url_for('blog.admin_article'))
        except:
            db.session.rollback()
            db.session.flush()
            return "添加失败"

    return render_template('admin/add-article.html',blog_type_list=blog_type_list)



# 后台删除文章接口
@blue.route('/admin/article/delete/', methods=["GET","POST"])
def admin_delete_article():
    if request.method == "POST":
        blogid = request.form.get("id")
        blog = Blog.query.get(blogid)
        try:
            db.session.delete(blog)
            db.session.commit()
            return "OK"
        except:
            db.session.rollback()
            db.session.flush()
            return "fail"


# 后台删除搜索文章接口
@blue.route('/admin/search/delete/', methods=["POST"])
def admin_delete_search():
    if request.method == "POST":
        blogid = request.form.get("id")
        blog = Blog.query.get(blogid)
        try:
            db.session.delete(blog)
            db.session.commit()
            return "OK"
        except:
            db.session.rollback()
            db.session.flush()
            return "fail"



# 后台批量删除文章接口，返回文章页面
@blue.route('/admin/deletelist', methods=['POST'])
def admin_deletelist():
    if request.method == "POST":
        blogid_list = request.form.getlist('checkbox[]')
        print(blogid_list)
        for id in blogid_list:
            blog = Blog.query.get(id)
            try:
                db.session.delete(blog)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
                return "fail"
        return redirect(url_for('blog.admin_article'))


# 后台删除博客类型接口
@blue.route('/admin/category/delete/', methods=["POST"])
def admin_delete_blogtype():
    if request.method == "POST":
        blogtypeid = request.form.get("id")
        print(blogtypeid)
        blogtype = BlogType.query.get(blogtypeid)
        blogs = Blog.query.filter(Blog.blog_type==blogtypeid)
        try:
            for blog in blogs:
                db.session.delete(blog)
            db.session.delete(blogtype)
            db.session.commit()


            return "OK"
        except:
            db.session.rollback()
            db.session.flush()
            return "fail"


# 后台博客分类管理页面
@blue.route('/admin/category/',methods=['GET','POST'])
def admin_category():
    if request.method =='POST':
        blog_type = BlogType()
        blog_type.typename = request.form.get('name')
        try:
            db.session.add(blog_type)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
            return 'fail'
        return redirect(url_for('blog.admin_category'))


    blog_types = BlogType.query.all()
    num_list = []
    for i in blog_types:
        x = Blog.query.filter(Blog.blog_type == i.id).count()
        num_list.append(x)
    content = {}
    print(num_list)
    content['blog_types'] = blog_types
    content['num_list'] = num_list

    return render_template('admin/category.html',content=content)


# 友情链接
@blue.route('/admin/flink/')
def admin_flink():
    return render_template('admin/flink.html')


# 公告
@blue.route('/admin/notice/')
def admin_notice():
    return render_template('admin/notice.html')


# 评论页面
@blue.route('/admin/comment/')
def admin_comment():
    return render_template('admin/comment.html')


#管理用户页面
@blue.route('/admin/manage_user/')
def admin_manage_user():
    return render_template('admin/manage-user.html')


# 登录日志
@blue.route('/admin/loginlog/')
def admin_loginlog():
    return render_template('admin/loginlog.html')


# 设置
@blue.route('/admin/setting/')
def admin_setting():
    return render_template('admin/setting.html')


# 阅读设置
@blue.route('/admin/readset/')
def admin_readset():
    return render_template('admin/readset.html')


