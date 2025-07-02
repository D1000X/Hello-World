let valores = [11,33,4,5];
valores.push(1)
valores.sort()

/*for (const pos in valores) {
    console.log(`a posição ${pos} tem valor ${valores[pos]} `)
} 
 for (let i = 0; i<valores.length;i++){
    console.log(`a posição ${i} tem valor ${valores[i]}`)
}*/
 
let pos = valores.indexOf(2)
if (pos == -1) {
    console.log(`o valor não foi encomtrado`)
}else{
    console.log(`O valor está na posição ${pos} `)
}
 


