/*
======================================================
ProjectStarter

documentation.js

======================================================
*/

const faqItems = document.querySelectorAll(".faq-item");

faqItems.forEach(item=>{

    item.querySelector("h3").addEventListener("click",()=>{

        if(item.classList.contains("active")){

            item.classList.remove("active");

        }

        else{

            faqItems.forEach(i=>{

                i.classList.remove("active");

            });

            item.classList.add("active");

        }

    });

});





/*=========================================
Animation d'apparition
=========================================*/

const cards = document.querySelectorAll(".doc-card");

const observer = new IntersectionObserver(entries=>{

    entries.forEach(entry=>{

        if(entry.isIntersecting){

            entry.target.animate([

                {

                    opacity:0,

                    transform:"translateY(40px)"

                },

                {

                    opacity:1,

                    transform:"translateY(0)"

                }

            ],{

                duration:500,

                fill:"forwards"

            });

        }

    });

});

cards.forEach(card=>{

    observer.observe(card);

});