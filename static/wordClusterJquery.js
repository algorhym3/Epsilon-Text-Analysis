
$("#BUTTON_16").click( function(event) {
  event.preventDefault();
  $.post(
    "http://127.0.0.1:5000/getList",
  $("#FORM_4").serializeArray(),
  function(info) {
      console.log(info);
      var parsed = JSON.parse(info);
      var list =  [[]]
      for(var x in parsed){
        parsed[x][1] = parsed[x][1];
        console.log(parsed[x][0])
        list.push(parsed[x]);
      }
      options = {
        gridSize: 25,
        minSize: 5 ,
        list: list,
        hover: window.drawBox ,
          rotateRatio: 0,
          // drawOutOfBound: true ,
  click: function(item) {
    alert(item[0] + ': ' + item[1]);
  },
  color: function() {
      return (['#00b6b9', '#ee3268', '#909090' ,'#fec255', '#7b347b'])[Math.floor(Math.random() * 5)]
    },
      };
      list[0]=['taher',1];
      console.log(list);
WordCloud(document.getElementById('my_canvas'), options );
  });
});
