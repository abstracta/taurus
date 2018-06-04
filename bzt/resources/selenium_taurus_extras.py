"""
Copyright 2018 BlazeMeter Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from string import Template as StrTemplate
from selenium.common.exceptions import NoSuchWindowException, NoSuchFrameException
from bzt.six import text_type


def drag_and_drop(driver, drag_element, drop_element):
    # https://github.com/html-dnd/html-dnd
    dnd = "var dnd,__extends=this&&this.__extends||function(t,e){for(var r in e)e.hasOwnProperty(r)&&(t[r]=e[r]);function i(){this.constructor=t}t.prototype=null===e?Object.create(e):(i.prototype=e.prototype,new i)};!function(t){\"use strict\";function u(t,e){var r=document.createEvent(\"CustomEvent\");return r.initCustomEvent(t,!0,!0,null),r.dataTransfer=e,r}t.simulate=function(t,e){var r=new c;r.mode=\"readwrite\";var i=new h(r),n=u(\"dragstart\",i);t.dispatchEvent(n),r.mode=\"readonly\";var s=u(\"dragover\",i);e.dispatchEvent(s);var o=u(\"drop\",i);e.dispatchEvent(o),r.mode=\"protected\";var a=u(\"dragend\",i);t.dispatchEvent(a)};var h=function(){function t(t){this.store=t,this.typeTable={},this.effectAllowed=\"uninitialized\",this.types=[],this.files=new e}return t.prototype.setDragImage=function(t,e,r){},t.prototype.getData=function(t){if(\"protected\"===this.store.mode)return\"\";var e=!1;if(\"text\"===(t=t.toLowerCase())?t=\"text/plain\":\"url\"===t&&(t=\"text/uri-list\",e=!0),!(t in this.typeTable))return\"\";var r=this.typeTable[t];return e&&(r=n(r)[0]||\"\"),r},t.prototype.setData=function(t,e){this.store&&\"readwrite\"===this.store.mode&&(\"text\"===(t=t.toLowerCase())?t=\"text/plain\":\"url\"===t&&(t=\"text/uri-list\"),this.typeTable[t]=e,this.types=Object.keys(this.typeTable))},t.prototype.clearData=function(t){var e=this;this.store&&\"readwrite\"===this.store.mode&&(void 0!==t?(\"text\"===(t=t.toLowerCase())?t=\"text/plain\":\"url\"===t&&(t=\"text/uri-list\"),delete this.typeTable[t],this.types=Object.keys(this.typeTable)):this.types.filter(function(t){return\"Files\"!==t}).forEach(function(t){return e.clearData(t)}))},t}();t.DataTransfer=h;var e=function(){function t(){this.length=0}return t.prototype.item=function(t){return null},t}();t.FileList=e;var c=function(){},r=function(){function t(t){this.store=t,this.items=[],this.typeTable={},this.length=0}return t.prototype.remove=function(t){if(\"readwrite\"!==this.store.mode)throw i.createByDefaultMessage();var e=this.items.splice(t,1)[0];this.syncInternal(),e&&delete this.typeTable[e.type]},t.prototype.clear=function(){if(\"readwrite\"!==this.store.mode)throw i.createByDefaultMessage();this.items=[],this.syncInternal()},t.prototype.add=function(t,e){if(\"readwrite\"!==this.store.mode)return null;if(\"string\"==typeof t){var r=e.toLowerCase();if(this.typeTable[r])throw o.createByDefaultMessage();var i=s.createForString(t,r,this.store);this.items.push(i),this.typeTable[r]=!0}else{var n=s.createForFile(t,this.store);this.items.push(n)}this.syncInternal()},t.prototype.syncInternal=function(){for(var r=this,t=0;t<this.length;t++)delete this[t];this.items.forEach(function(t,e){r[e]=t}),this.length=this.items.length},t}();t.DataTransferItemList=r;var s=function(){function i(t,e,r,i){this.data=t,this.store=i,this.type=r,this.kind=e}return i.prototype.getAsString=function(t){var e=this;t||\"readwrite\"===this.store.mode&&\"string\"===this.kind&&setTimeout(function(){t(e.data)},0)},i.prototype.getAsFile=function(){return\"readwrite\"!==this.store.mode?null:\"string\"!==this.kind?null:this.data},i.createForString=function(t,e,r){return new i(t,\"string\",e,r)},i.createForFile=function(t,e){return new i(t,\"file\",null,e)},i}(),i=function(e){function t(t){e.call(this,t),this.message=t,this.name=\"InvalidStateError\"}return __extends(t,e),t.createByDefaultMessage=function(){return new t(\"The object is in an invalid state\")},t}(Error),o=function(e){function t(t){e.call(this,t),this.message=t,this.name=\"NotSupportedError\"}return __extends(t,e),t.createByDefaultMessage=function(){return new i(\"The operation is not supported\")},t}(Error);function n(t){return\"\"===(t=t.replace(/\\r\\n$/,\"\"))?[]:t.split(/\\r\\n/).filter(function(t){return\"#\"!==t[0]})}t.parseTextUriList=n}(dnd||(dnd={}));"
    return driver.execute_script('%s;dnd.simulate(arguments[0], arguments[1]);' % dnd, drag_element, drop_element)

class Apply(StrTemplate):

    def __init__(self, template):
        super(Apply, self).__init__(template)
        self.variables = {}

    def __repr__(self):
        return repr(self.safe_substitute(self.variables))

    def __str__(self):
        return self.safe_substitute(self.variables)


class Template:

    def __init__(self, variables):
        self.variables = variables
        self.tmpl = Apply("")

    def apply(self, template):
        self.tmpl.template = template
        self.tmpl.variables = self.variables
        return text_type(self.tmpl)

    @staticmethod
    def str_repr(text):
        return repr(text)[1:] if repr(text)[0] == "u" else repr(text)


class FrameManager:

    def __init__(self, driver):
        self.driver = driver
    
    def switch(self, frame_name=None):
        try:
            if not frame_name or frame_name == "relative=top":
                self.driver.switch_to_default_content()
            elif frame_name.startswith("index="):  # Switch using index frame using relative position
                self.driver.switch_to.frame(int(frame_name.split("=")[1]))
            elif frame_name == "relative=parent":  # Switch to parent frame of the current frame
                self.driver.switch_to.parent_frame()
            else:  # Use the selenium alternative
                self.driver.switch_to.frame(frame_name)
        except NoSuchFrameException:
            raise NoSuchFrameException("Invalid Frame ID: %s" % frame_name)


class WindowManager:

    def __init__(self, driver):
        self.driver = driver
        self.windows = {}

    def switch(self, window_name=None):
        try:
            if not window_name:  # Switch to last window created
                self.driver.switch_to.window(self.driver.window_handles[-1])
            else:
                if window_name.isdigit():  # Switch to window handler index
                    self._switch_by_idx(int(window_name))
                else:
                    if window_name.startswith("win_ser_"):  # Switch using window sequential mode
                        self._switch_by_win_ser(window_name)
                    else:  # Switch using window name
                        self.driver.switch_to.window(window_name)
        except NoSuchWindowException:
            raise NoSuchWindowException("Invalid Window ID: %s" % window_name)

    def _switch_by_idx(self, win_index):
        wnd_handlers = self.driver.window_handles
        if len(wnd_handlers) <= win_index and win_index >= 0:
            self.driver.switch_to.window(wnd_handlers[win_index])
        else:
            raise NoSuchWindowException("Invalid Window ID: %s" % str(win_index))

    def _switch_by_win_ser(self, window_name):
        if window_name == "win_ser_local":
            wnd_handlers = self.driver.window_handles
            if len(wnd_handlers) > 0:
                self.driver.switch_to.window(wnd_handlers[0])
            else:
                raise NoSuchWindowException("Invalid Window ID: %s" % window_name)
        else:
            if window_name not in self.windows:
                self.windows[window_name] = self.driver.window_handles[-1]
            self.driver.switch_to.window(self.windows[window_name])

    def close(self, window_name=None):
        if window_name:
            self.switch(window_name)
        self.driver.close()
