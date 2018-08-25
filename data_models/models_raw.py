# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Numeric, String, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class AppClaim(Base):
    __tablename__ = 'app_claim'

    app_claim_id = Column(Integer, primary_key=True, server_default=text("nextval('app_claim_id_seq'::regclass)"))
    claim_name = Column(String(100), nullable=False, unique=True)


class AppRole(Base):
    __tablename__ = 'app_role'

    app_role_id = Column(Integer, primary_key=True, server_default=text("nextval('app_role_id_seq'::regclass)"))
    role_name = Column(String(100), nullable=False, unique=True)


class AppUser(Base):
    __tablename__ = 'app_user'

    app_user_id = Column(Integer, primary_key=True, server_default=text("nextval('app_user_id_seq'::regclass)"))
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    phonenumber = Column(String(20))
    email = Column(String(100), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)
    is_restricted = Column(Boolean, nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))


class AppUserAppClaim(Base):
    __tablename__ = 'app_user_app_claim'

    app_user_id = Column(ForeignKey('app_user.app_user_id'), primary_key=True, nullable=False)
    app_claim_id = Column(ForeignKey('app_claim.app_claim_id'), primary_key=True, nullable=False)
    claim_value = Column(String)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    app_claim = relationship('AppClaim')
    app_user = relationship('AppUser')


class AppUserAppRole(Base):
    __tablename__ = 'app_user_app_role'

    app_user_id = Column(ForeignKey('app_user.app_user_id'), primary_key=True, nullable=False)
    app_role_id = Column(ForeignKey('app_role.app_role_id'), primary_key=True, nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    app_role = relationship('AppRole')
    app_user = relationship('AppUser')


class AppUserApplication(Base):
    __tablename__ = 'app_user_application'

    app_user_id = Column(ForeignKey('app_user.app_user_id'), primary_key=True, nullable=False)
    application_id = Column(ForeignKey('application.application_id'), primary_key=True, nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    app_user = relationship('AppUser')
    application = relationship('Application')


class Application(Base):
    __tablename__ = 'application'

    application_id = Column(Integer, primary_key=True, server_default=text("nextval('application_id_seq'::regclass)"))
    application_name = Column(String(250), nullable=False, unique=True)


class Article(Base):
    __tablename__ = 'article'

    article_id = Column(Integer, primary_key=True, server_default=text("nextval('article_id_seq'::regclass)"))
    app_user_id = Column(ForeignKey('app_user.app_user_id'), nullable=False)
    article_group_id = Column(ForeignKey('article_group.article_group_id'))
    title = Column(String(150), nullable=False)
    content = Column(Text, nullable=False)
    date_to_publish = Column(DateTime(True))
    promoted_start_date = Column(DateTime(True))
    promoted_end_date = Column(DateTime(True))
    comments_enabled = Column(Boolean, nullable=False, server_default=text("false"))
    price = Column(Numeric)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    app_user = relationship('AppUser')
    article_group = relationship('ArticleGroup')


class ArticleApplication(Base):
    __tablename__ = 'article_application'

    article_id = Column(ForeignKey('article.article_id'), primary_key=True, nullable=False)
    application_id = Column(ForeignKey('application.application_id'), primary_key=True, nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    application = relationship('Application')
    article = relationship('Article')


class ArticleComment(Base):
    __tablename__ = 'article_comment'

    article_comment_id = Column(Integer, primary_key=True, server_default=text("nextval('article_comment_id_seq'::regclass)"))
    article_id = Column(ForeignKey('article.article_id'), nullable=False)
    app_user_id = Column(ForeignKey('app_user.app_user_id'), nullable=False)
    parent_id = Column(ForeignKey('article_comment.article_comment_id'))
    comment = Column(String(1000), nullable=False)
    is_flagged = Column(Boolean, nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    updated_date = Column(DateTime(True), nullable=False, server_default=text("now()"))
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))

    app_user = relationship('AppUser')
    article = relationship('Article')
    parent = relationship('ArticleComment', remote_side=[article_comment_id])


class ArticleGroup(Base):
    __tablename__ = 'article_group'

    article_group_id = Column(Integer, primary_key=True, server_default=text("nextval('article_group_id_seq'::regclass)"))
    title = Column(String(150), nullable=False)
    show_all_links = Column(Boolean, nullable=False)
    is_deleted = Column(Boolean, nullable=False, server_default=text("false"))


class ArticleTag(Base):
    __tablename__ = 'article_tag'

    article_id = Column(ForeignKey('article.article_id'), primary_key=True, nullable=False)
    tag_id = Column(ForeignKey('tag.tag_id'), primary_key=True, nullable=False)
    created_date = Column(DateTime(True), nullable=False, server_default=text("now()"))

    article = relationship('Article')
    tag = relationship('Tag')


class Tag(Base):
    __tablename__ = 'tag'

    tag_id = Column(Integer, primary_key=True, server_default=text("nextval('tag_id_seq'::regclass)"))
    tag_name = Column(String(100), nullable=False, unique=True)
