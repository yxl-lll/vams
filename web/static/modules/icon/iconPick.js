layui.define(['jquery', 'laypage', 'dropdown', 'element'], function (exports) {
    let $ = layui.jquery,
        laypage = layui.laypage,
        element = layui.element,
        dropdown = layui.dropdown;

    let self = {};

    /**
     *
     * @param config
     * @returns {*|boolean}
     * config.el 渲染位置
     * config.on 选中后的操作
     */
    self.init = function (config) {
        let ex_config = config;
        let dom = config.el;
        if (!dom) {
            console.error('渲染参数不能为空')
            return false;
        }
        dropdown.render({
            elem: dom,
            className: 'icon-dropdown',
            content:
                `<div class="layui-tab layui-tab-brief" lay-filter="icon-tabs" style="margin: 0">
                    <ul class="layui-tab-title">
                        <li class="layui-this" lay-id="wireframe">线框风格</li>
                        <li class="" lay-id="solid">实底风格</li>
                        <li class="" lay-id="brand">品牌商标</li>
                    </ul>
                    <div class="layui-tab-content" style="flex: none;width: 100%;outline: none;padding: 0;">
                       <div class="layui-tab-item layui-show">
                         <div id="icon-content" 
                         style="
                         height: 300px;width: 300px;
                         display: grid;gap: 0.5rem;
                         border-radius: 2px;background-color: #f5f5f5;
                         padding: 0.5rem;font-size: 18px;line-height: 1.57142857;justify-items: center;grid-template-columns: repeat(6, minmax(0px, 1fr));"
                         ></div>
                         <div id="icon-page" style="text-align: center;"></div>
                       </div>
                    </div>
                </div>`,
            ready: function () {
                loadIcon('wireframe');
                element.on('tab(icon-tabs)', function () {
                    let attr = $(this).attr('lay-id');
                    loadIcon(attr);
                })
            }
        })

        function loadIcon(type) {
            let list = [];
            switch (type) {
                case 'solid':
                    list = icon_solid;
                    break;
                case 'brand':
                    list = icon_brand;
                    break;
                case 'wireframe':
                default:
                    list = icon_wireframe;
                    break;
            }

            laypage.render({
                elem: 'icon-page',
                count: list.length,
                groups: 2,
                first: false,
                last: false,
                layout: ['prev', 'page', 'next', 'count'],
                limit: 36,
                jump: function (obj) {
                    let content = $('#icon-content');
                    content.empty();
                    const thisData = list.concat().splice(obj.curr * obj.limit - obj.limit, obj.limit);
                    (thisData || []).forEach(item => {
                        let iconItem =
                            `<div class="layui-icon-card" lay-icon="${item.name}" style="
                                border-width: 1px;border-style: solid;border-color: transparent; border-radius: 4px;background-color: #ffff;justify-content: center;
                                align-items: center;cursor: pointer;width: 2.5rem;height: 2.5rem;display: flex;
                                ">
                             <div class="layui-icon-item">
                                <span class="layui-icon ${item.name}" style="font-size: 20px;"></span>
                             </div>
                            </div>`
                        let $iconItem = $(iconItem);
                        $iconItem.hover(function () {
                            $iconItem.css('border-color', 'let(--blue-6)')
                        }, function () {
                            $iconItem.css('border-color', 'transparent')
                        })
                        $iconItem.off('click').on('click', function () {
                            ex_config.on(item.name)
                        })
                        content.append($iconItem);
                    })
                }
            })
        }

        return ex_config;
    }

    exports('icon', self);
})
