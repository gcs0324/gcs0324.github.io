(function(){
  var pages=[
    {href:'design-outline.html',label:'导航'},
    {href:'design-01-creational.html',label:'01 创建型'},
    {href:'design-02-structural.html',label:'02 结构型'},
    {href:'design-03-behavioral.html',label:'03 行为型'},
    {href:'design-04-system.html',label:'04 系统设计'},
    {href:'design-05-interview.html',label:'05 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="design-outline.html">设计 ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
