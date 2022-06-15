function changeColor(){
    let form = document.getElementById('changecolorform')
    form.addEventListener('submit', form.submit())
}


// create a function to check if checkbox is checked
function checkboxChecked(){
    let checkbox = document.getElementById('flexSwitchCheckChecked')
    
    if (checkbox.getAttributeNames().includes('checked')){
        // Set body color to black
        document.body.style.backgroundColor = 'black'

        // Set navbar color black and text to white
        let nav = document.getElementById('main_nav')
        nav.classList.remove('bg-light')
        nav.classList.add('bg-dark', 'text-white')

        // Set navbar elements color to white
        let nav_elements = document.getElementsByClassName('nav-link active')
        for(let i of nav_elements) i.classList.add('text-white')

        // Set all h4 tag texts to white
        // h4 tags and buttons from index page
        let h4 = document.getElementsByTagName('h4')
        let buttons = document.getElementsByTagName('button')
        for(let i of h4) i.classList.add('text-white')
        for(let i of buttons) i.classList.add('text-white')

        // Change text colors from details page

        let p = document.getElementsByTagName('p')
        let label = document.getElementsByTagName('label')
        let comment = document.getElementById('submit')
        for(let i of p) i.classList.add('text-white')
        for(let i of label) i.classList.add('text-white')
        comment.classList.add('text-white')
        
    }
}

checkboxChecked()
