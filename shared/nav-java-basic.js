(function(){
  var pages=[
    {href:'java-basic-outline.html',label:'导航'},
    {href:'java-basic-01-oop.html',label:'01 OOP'},
    {href:'java-basic-02-collection.html',label:'02 集合'},
    {href:'java-basic-03-generic.html',label:'03 泛型'},
    {href:'java-basic-04-exception.html',label:'04 异常IO'},
    {href:'java-basic-05-jdk8.html',label:'05 JDK8'},
    {href:'java-basic-06-interview.html',label:'06 面试题'}
  ];
  var cur=location.pathname.split('/').pop();
  var links=pages.map(function(p){return '<a href="'+p.href+'"'+(cur===p.href?' class="active"':'')+'>'+p.label+'</a>';}).join('');
  var nav='<div class="topnav"><a class="topnav-brand" href="java-basic-outline.html">基础 ·</a><div class="topnav-links">'+links+'</div></div>';
  document.currentScript.insertAdjacentHTML('afterend',nav);
})();
