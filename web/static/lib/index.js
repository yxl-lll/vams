/**

 @Name：layuiAdmin iframe版主入口
 @Author：贤心
 @Site：http://www.layui.com/admin/
 @License：LPPL
    
 */

 Date.prototype.format = function (fmt) {
  var o = {
      "M+": this.getMonth() + 1, //月份
      "d+": this.getDate(), //日
      "h+": this.getHours(), //小时
      "m+": this.getMinutes(), //分
      "s+": this.getSeconds(), //秒
      "q+": Math.floor((this.getMonth() + 3) / 3), //季度
      "S": this.getMilliseconds() //毫秒
  };
  if (/(y+)/.test(fmt)) {
      fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
  }
  for (var k in o) {
      if (new RegExp("(" + k + ")").test(fmt)) {
          fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
      }
  }
  return fmt;
}
layui.extend({
  setter: 'config' //配置模块
  , admin: 'lib/admin' //核心模块
  , view: 'lib/view' //视图渲染模块
}).define(['setter', 'admin'], function (exports) {
  var setter = layui.setter
    , element = layui.element
    , admin = layui.admin
    , tabsPage = admin.tabsPage
    , view = layui.view

    //打开标签页
    , openTabsPage = function (url, text) {
      //遍历页签选项卡
      var matchTo
        , tabs = $('#main_app_tabsheader>li')
        , path = url.replace(/(^http(s*):)|(\?[\s\S]*$)/g, '');

      tabs.each(function (index) {
        var li = $(this)
          , layid = li.attr('lay-id');

        if (layid === url) {
          matchTo = true;
          tabsPage.index = index;
        }
      });

      text = text || '新标签页';

      if (setter.pageTabs) {
        //如果未在选项卡中匹配到，则追加选项卡
        if (!matchTo) {
          //延迟修复 Firefox 空白问题
          setTimeout(function () {
            $(APP_BODY).append([
              '<div class="layadmin-tabsbody-item layui-show">'
              , '<iframe src="' + url + '" frameborder="0" class="layadmin-iframe"></iframe>'
              , '</div>'
            ].join(''));
          }, 10);

          tabsPage.index = tabs.length;
          element.tabAdd(FILTER_TAB_TBAS, {
            title: '<span>' + text + '</span>'
            , id: url
            , attr: path
          });

        }
      } else {
        var iframe = admin.tabsBody(admin.tabsPage.index).find('.layadmin-iframe');
        iframe[0].contentWindow.location.href = url;
      }

      //定位当前tabs
      element.tabChange(FILTER_TAB_TBAS, url);
      admin.tabsBodyChange(tabsPage.index, {
        url: url
        , text: text
      });
    }

    , APP_BODY = '#main_app_body', FILTER_TAB_TBAS = 'layadmin-layout-tabs'
    , $ = layui.$, $win = $(window);

  //初始
  if (admin.screen() < 2) admin.sideFlexible();

  //将模块根路径设置为 controller 目录
  layui.config({
    base: setter.base + 'modules/'
  });

  //扩展 lib 目录下的其它模块
  layui.each(setter.extend, function (index, item) {
    var mods = {};
    mods[item] = '{/}' + setter.base + 'lib/extend/' + item;
    layui.extend(mods);
  });

  view().autoRender();

  //加载公共模块
  layui.use('common');

  //对外输出
  exports('index', {
    openTabsPage: openTabsPage
  });
});
