(function(){
  // ---- helpers ----
  function csrftokenFromCookie(){
    const m = document.cookie.match(/(?:^|; )csrftoken=([^;]+)/);
    return m ? decodeURIComponent(m[1]) : '';
  }
  async function apiGet(url){
    const r = await fetch(url, {credentials:'same-origin'});
    if(!r.ok) throw new Error('GET '+url+' '+r.status);
    return r.json();
  }
  async function apiPost(url, payload){
    const r = await fetch(url, {
      method:'POST',
      headers: {
        'Content-Type':'application/json',
        'X-CSRFToken': csrftokenFromCookie()
      },
      body: JSON.stringify(payload),
      credentials:'same-origin'
    });
    if(!r.ok) throw new Error('POST '+url+' '+r.status);
    return r.json();
  }
  function fillSelect(sel, items, opts){
    const keepFirst = opts && opts.keepFirst;
    const selectedId = opts && opts.selectedId;
    if(!keepFirst) sel.innerHTML = '';
    if(!keepFirst){
      const o0 = document.createElement('option');
      o0.value=''; o0.textContent='---------';
      sel.appendChild(o0);
    }
    items.forEach(it=>{
      const o = document.createElement('option');
      o.value = it.id; o.textContent = it.name;
      if(selectedId && String(selectedId)===String(it.id)) o.selected = true;
      sel.appendChild(o);
    });
  }

  // ---- link form fields: type -> category ----
  async function refreshCategories(typeSel, catSel){
    const t = typeSel.value;
    fillSelect(catSel, [], {keepFirst:false});
    if(!t) return;
    const data = await apiGet('/api/categories/?type='+encodeURIComponent(t));
    fillSelect(catSel, data);
  }
  // ---- link form fields: category -> subcategory ----
  async function refreshSubcategories(catSel, subSel){
    const c = catSel.value;
    fillSelect(subSel, [], {keepFirst:false});
    if(!c) return;
    const data = await apiGet('/api/subcategories/?category='+encodeURIComponent(c));
    fillSelect(subSel, data);
  }

  document.addEventListener('DOMContentLoaded', ()=>{
    // Form page hooks
    const typeSel = document.getElementById('form-type');
    const catSel  = document.getElementById('form-category');
    const subSel  = document.getElementById('form-subcategory');

    if(typeSel && catSel){
      typeSel.addEventListener('change', async ()=>{
        await refreshCategories(typeSel, catSel);
        if(subSel) fillSelect(subSel, [], {keepFirst:false});
      });
    }
    if(catSel && subSel){
      catSel.addEventListener('change', async ()=>{
        await refreshSubcategories(catSel, subSel);
      });
    }

      // ---- inline create buttons (modals) ----
      function byId(id){ return document.getElementById(id); }
      const btnAddStatus = byId('btn-add-status');
      const btnAddType   = byId('btn-add-type');
      const btnAddCat    = byId('btn-add-category');
      const btnAddSub    = byId('btn-add-subcategory');

      // micro-modal impl (no Bootstrap JS dependency)
      function openModal(id){ byId(id).classList.remove('d-none'); }
      function closeModal(id){ byId(id).classList.add('d-none'); }

      // Buttons -> open modals
      if(btnAddStatus) btnAddStatus.addEventListener('click', ()=>openModal('modal-status'));
      if(btnAddType)   btnAddType.addEventListener('click',   ()=>openModal('modal-type'));
      if(btnAddCat)    btnAddCat.addEventListener('click',    ()=>openModal('modal-category'));
      if(btnAddSub)    btnAddSub.addEventListener('click',    ()=>openModal('modal-subcategory'));

      // Close handlers
      document.querySelectorAll('[data-close-modal]').forEach(el=>{
        el.addEventListener('click', ()=> closeModal(el.dataset.closeModal));
      });

      // Submit handlers
      const formStatus = byId('form-modal-status');
      const formType   = byId('form-modal-type');
      const formCat    = byId('form-modal-category');
      const formSub    = byId('form-modal-subcategory');

      if(formStatus){
        formStatus.addEventListener('submit', async (e)=>{
          e.preventDefault();
          const name = e.target.name.value.trim();
          if(!name) return;
          const obj = await apiPost('/api/statuses/', {name});
          const select = document.querySelector('select[name="status"]');
          const o = new Option(obj.name, obj.id, true, true);
          select.add(o);
          closeModal('modal-status');
          e.target.reset();
        });
      }

      if(formType){
        formType.addEventListener('submit', async (e)=>{
          e.preventDefault();
          const name = e.target.name.value.trim();
          if(!name) return;
          const obj = await apiPost('/api/types/', {name});
          const select = document.getElementById('form-type');
          const o = new Option(obj.name, obj.id, true, true);
          select.add(o);
          // сброс категорий/подкатегорий
          if(catSel){ await refreshCategories(select, catSel); }
          if(subSel){ fillSelect(subSel, [], {keepFirst:false}); }
          closeModal('modal-type');
          e.target.reset();
        });
      }

      if(formCat){
        formCat.addEventListener('submit', async (e)=>{
          e.preventDefault();
          const name = e.target.name.value.trim();
          const type_id = typeSel ? typeSel.value : '';
          if(!name || !type_id) { alert('Сначала выберите тип'); return; }
          const obj = await apiPost('/api/categories/', {name, type: Number(type_id)});
          // обновляем селект категорий, выбираем новую
          if(catSel){
            await refreshCategories(typeSel, catSel);
            catSel.value = String(obj.id);
          }
          if(subSel){ fillSelect(subSel, [], {keepFirst:false}); }
          closeModal('modal-category');
          e.target.reset();
        });
      }

      if(formSub){
        formSub.addEventListener('submit', async (e)=>{
          e.preventDefault();
          const name = e.target.name.value.trim();
          const category_id = catSel ? catSel.value : '';
          if(!name || !category_id) { alert('Сначала выберите категорию'); return; }
          const obj = await apiPost('/api/subcategories/', {name, category: Number(category_id)});
          // обновляем подкатегории
          if(subSel){
            await refreshSubcategories(catSel, subSel);
            subSel.value = String(obj.id);
          }
          closeModal('modal-subcategory');
          e.target.reset();
        });
      }
  });
})();
