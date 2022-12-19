# Changelog

<!--next-version-placeholder-->

## v2.0.6 (2022-12-19)
### Fix
* **drf:** Prevent translation deletion on update with PATCH method ([`f645b14`](https://github.com/lotrekagency/django-hvad/commit/f645b14bc40342ad9a09b69cc1d5378d1a220e70))

## v2.0.5 (2022-10-25)
### Fix
* Run validation on translations list consistent with language ([`781c6ea`](https://github.com/lotrekagency/django-hvad/commit/781c6ea8b183a223333c0a1f5d2f69fa43d5f274))

## v2.0.4 (2022-10-17)
### Fix
* Fixed recursion errors for models with bads str functions ([`2059deb`](https://github.com/lotrekagency/django-hvad/commit/2059debc85e194b53835b4e1d2ec57b3aabaff1c))

## v2.0.3 (2022-10-06)
### Fix
* Fix some django 4.1 compability issues ([`11ef233`](https://github.com/lotrekagency/django-hvad/commit/11ef23387573f5af5bf8631c5722aa2c9451246a))
* Fix clean_fields to return a list ([`9a18171`](https://github.com/lotrekagency/django-hvad/commit/9a181715a35b83af45a1c0da797470a9b4798bba))
* Fix clean_fields concat set and lists ([`7a247c2`](https://github.com/lotrekagency/django-hvad/commit/7a247c2e488f17b9b9eb9b0fed1224e27b7c7099))
* Fix django model serializable_value not catching for WrongManager exception ([`34abd77`](https://github.com/lotrekagency/django-hvad/commit/34abd77fabe3e455f04d24e668314f612e6bd8fa))
* **rest_framework:** Fixed TranslatableModelMixin build_fields() method building only standard field ([`23095fb`](https://github.com/lotrekagency/django-hvad/commit/23095fb9734f7f7f2c000b10fa57e5a74d925bd3))

## v2.0.2 (2022-08-10)
### Fix
* **drf:** Pass instance to serializers for uniqueness validations ([`1c45caa`](https://github.com/lotrekagency/django-hvad/commit/1c45caa6fa6fe26e8a2ccf9ff82af6fd60cebf33))

## v2.0.1 (2022-05-19)
### Fix
* Added missing methods to SingleTranslationObject to make it work with django 4 ([`b6bae7c`](https://github.com/lotrekagency/django-hvad/commit/b6bae7c381844e34e884e3f61448c36fed94d7f5))

## v2.0.0 (2022-05-12)
### Fix
* Query._filter_or_exclude to work from django 2 to django 4 ([`910374d`](https://github.com/lotrekagency/django-hvad/commit/910374d88593808a35a38c6d2a5edaa3d88c978a))
* Query._filter_or_exclude to work with django 4 ([`875ca4d`](https://github.com/lotrekagency/django-hvad/commit/875ca4d203a2b1b49b8f159fca9b96fe35169bd7))
* Query.add_filter to work with django 3 and django 4 ([`985b488`](https://github.com/lotrekagency/django-hvad/commit/985b488099aff99544a6a1a5d8b8e98ae80bff51))
* Fix Query.clear_ordering args to fix django 4 compatibility ([`129be00`](https://github.com/lotrekagency/django-hvad/commit/129be0002eaad3762385e75f979c0180e40c905b))
* Fix args of get_extra_restriction for django 4 compatibility ([`d185e8f`](https://github.com/lotrekagency/django-hvad/commit/d185e8f178f09500ca244f8955624fbaf59e2b1a))
* Fix add_filter args for django 4 support ([`b924092`](https://github.com/lotrekagency/django-hvad/commit/b9240926139f25ed49bd01f1f065c882970a4333))
* Fix WhereNode import for django 4 ([`c060be7`](https://github.com/lotrekagency/django-hvad/commit/c060be7b92d0a9883a8112347e6ba715631c6078))

## v1.8.1 (2021-10-26)

