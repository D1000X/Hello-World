const objs=document.getElementsByTagName('div')
let num=[10,20,30,40,50];
for(n of objs){
    console.log(n.innerHTML='curso')
}

for(n in objs){
    console.log(num[n])
}
//for (let i=0;i<num.length;i++){
  //  console.log(num[i])
//}
