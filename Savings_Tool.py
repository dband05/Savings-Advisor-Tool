#######____MAIN FRAME_____######

import tkinter as tk 
from tkinter import *
from tkinter import ttk 
import sqlite3
from tabulate import tabulate


global database_file
global post_retire_opt
global start

#create start window   
#def window_edit_item():
start = Tk()
start.title('Getting Started')
start.geometry("400x400")

#create text boxes
database_file = Entry(start, width=30)
database_file.insert(END, 'Sample_Savings.sqlite')
database_file.grid(row=0, column = 1, padx=20, pady=(10,0))

post_retire = IntVar()
post_retire_opt = Checkbutton(start, onvalue=1, offvalue=0, variable=post_retire)
post_retire_opt.grid(row=2, column = 1, padx=20, pady=(10,0))

#create text box labels
database_file_label = Label(start, text = "Sqlite File Name")
database_file_label.grid(row = 0, column = 0, pady=(10,0))

post_retire_opt_label = Label(start, text = "Post-Retirement Analysis")
post_retire_opt_label.grid(row = 2, column = 0, pady=(10,0))


def lets_go():

    global database
    database = str(database_file.get())
    global post_retire1
    post_retire1 = int(post_retire.get())
    #print (database)
    #print(post_retire1)

    start.destroy()

    root = tk.Tk()

    root.title('Savings Tool')
    root.geometry("400x400")
    tabControl = ttk.Notebook(root)

    tab1 = ttk.Frame(tabControl) 
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl) 
      
    tabControl.add(tab1, text ='Methods') 
    tabControl.add(tab2, text ='Items')
    tabControl.add(tab3, text ='Calculate')
    tabControl.pack(expand = 1, fill ="both")

    #Datebases
    conn = sqlite3.connect(database)
    c = conn.cursor()

        
    #################____ITEMS TAB____##############################


    #create add fuction
    def add_item():
        #create db connection
        conn = sqlite3.connect(database)
        c = conn.cursor()

        #insert into table
        c.execute('''
        insert into ITEMS (ITEM,TERM,F_GOAL)
        values (:ITEM, :TERM, :F_GOAL)
        ''',
            {
                'ITEM': item_name_add.get(),
                'TERM': years_away_add.get(),
                'F_GOAL': target_amt_add.get()
            })
            
        #commit and close
        conn.commit()
        conn.close

        add.destroy()

    #create add window
    def window_add_item():
        global add
        add = Tk()
        add.title('Add a Record')
        add.geometry("400x400")

        #create global variables
        global item_name_add
        global target_amt_add
        global years_away_add
        
        #create text boxes
        item_name_add = Entry(add, width=30)
        item_name_add.grid(row=0, column = 1, padx=20, pady=(10,0))

        target_amt_add = Entry(add, width=30)
        target_amt_add.grid(row=1, column = 1)

        years_away_add = Entry(add, width=30)
        years_away_add.grid(row=2, column = 1)

        
        #create text box labels
        item_name_label = Label(add, text = "Item Name")
        item_name_label.grid(row = 0, column = 0, pady=(10,0))

        target_amt_label = Label(add, text = "Target Amt")
        target_amt_label.grid(row = 1, column = 0)

        years_away_label = Label(add, text = "Years Out")
        years_away_label.grid(row = 2, column = 0)

        #create save button
        save_btn = Button(add, text="Add Record",command=add_item)
        save_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx=143)



    #create edit fuction
    def edit_item():
        #create db connection
        conn = sqlite3.connect(database)
        c = conn.cursor()

        record_id = delete_box1.get()
        c.execute('''
        update ITEMS
        set ITEM = :Item
        ,F_GOAL = :Goal
        ,TERM = :Term
        where ID = :ID
        ''',
        {
        'Item': item_name_editor.get(),
        'Goal': target_amt_editor.get(),
        'Term': years_away_editor.get(),
        'ID': record_id
        }
         )
        
        #commit and close
        conn.commit()
        conn.close

        editor.destroy()

    #create edit window   
    def window_edit_item():
        global editor
        editor = Tk()
        editor.title('Update a Record')
        editor.geometry("400x400")

        #create global variables
        global item_name_editor
        global target_amt_editor
        global years_away_editor
        
        #create text boxes
        item_name_editor = Entry(editor, width=30)
        item_name_editor.grid(row=0, column = 1, padx=20, pady=(10,0))

        target_amt_editor = Entry(editor, width=30)
        target_amt_editor.grid(row=1, column = 1)

        years_away_editor = Entry(editor, width=30)
        years_away_editor.grid(row=2, column = 1)

        
        #create text box labels
        item_name_label = Label(editor, text = "Item Name")
        item_name_label.grid(row = 0, column = 0, pady=(10,0))

        target_amt_label = Label(editor, text = "Target Amt")
        target_amt_label.grid(row = 1, column = 0)

        years_away_label = Label(editor, text = "Years Out")
        years_away_label.grid(row = 2, column = 0)

        #create db connection
        conn = sqlite3.connect(database)
        c = conn.cursor()

        record_id = delete_box1.get()
        #qry db
        c.execute('''
        select ITEM, F_GOAL, TERM from ITEMS where ID = ''' + record_id)
        records = c.fetchall()
        #loop thru results
        for record in records:
            item_name_editor.insert(0,record[0])
            target_amt_editor.insert(0,record[1])
            years_away_editor.insert(0,record[2])
       
        
        #commit and close
        conn.commit()
        conn.close

        #create save button
        save_btn = Button(editor, text="Save Record",command=edit_item)
        save_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx=143)



    #create function to delete a record
    def delete_item():
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("delete from ITEMS where ID = " + delete_box1.get())

        #clear text boxes
        delete_box1.delete(0,END)

        #commit and close
        conn.commit()
        conn.close

        
    #create view function
    def view_item():
        # Datebases
        conn = sqlite3.connect(database)
        c = conn.cursor()

        #reset auto increment
        c.execute('''
        UPDATE sqlite_sequence SET SEQ=0 WHERE NAME="ITEMS";
        ''')
        
        c.execute('''
        select ID,ITEM,F_GOAL,TERM from ITEMS order by Term
        ''')
        records = c.fetchall()
        print(tabulate(list(records),headers=["ID","Item","Goal Amt","Term"]))
        
        #commit and close
        conn.commit()
        conn.close


    #DISPLAY#

    #view button
    query_btn = Button(tab2, text="Show records",command=view_item)
    query_btn.grid(row = 0, column = 0)
    #query_btn.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx=100)

    #create submit button
    submit_btn = Button(tab2, text = "Add record to database", command=window_add_item)
    submit_btn.grid(row = 1, column = 0)

    #ID Field
    delete_box_label = Label(tab2, text = "Select ID")
    delete_box_label.grid(row=2, column=0)

    delete_box1 = Entry(tab2, width=10)
    delete_box1.grid(row=2, column=1)

    #create delete button
    delete_btn = Button(tab2, text="Delete Record",command=delete_item)
    delete_btn.grid(row = 3, column = 0)

    #create update button
    edit_btn = Button(tab2, text="Edit Record",command=window_edit_item)
    edit_btn.grid(row = 4, column = 0)


    ################____METHODS_TAB_____#####################


    #create add fuction
    def add_meth():
        #create db connection
        conn = sqlite3.connect(database)
        c = conn.cursor()

        #insert into table
        c.execute('''
        insert into METHODS (METHOD,AVG_i,RISK_F)
        values (:METHOD, :AVG_i, :RISK_F)
        ''',
            {
                'METHOD': meth_name_add.get(),
                'AVG_i': interest_rate_add.get(),
                'RISK_F': risk_fact_add.get()
            })
            
        #commit and close
        conn.commit()
        conn.close

        add.destroy()

    #create add window
    def window_add_meth():
        global add
        add = Tk()
        add.title('Add a Record')
        add.geometry("400x400")

        #create global variables
        global meth_name_add
        global interest_rate_add
        global risk_fact_add
        
        #create text boxes
        meth_name_add = Entry(add, width=30)
        meth_name_add.grid(row=0, column = 1, padx=20, pady=(10,0))

        interest_rate_add = Entry(add, width=30)
        interest_rate_add.grid(row=1, column = 1)

        risk_fact_add = Entry(add, width=30)
        risk_fact_add.grid(row=2, column = 1)

        
        #create text box labels
        meth_name_label = Label(add, text = "Method Description")
        meth_name_label.grid(row = 0, column = 0, pady=(10,0))

        interest_rate_label = Label(add, text = "Average Interest Rate")
        interest_rate_label.grid(row = 1, column = 0)

        risk_fact_label = Label(add, text = "Risk Factor")
        risk_fact_label.grid(row = 2, column = 0)

        #create save button
        save_btn = Button(add, text="Add Record",command=add_meth)
        save_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx=143)



    #create edit fuction
    def edit_meth():
        #create db connection
        conn = sqlite3.connect(database)
        c = conn.cursor()

        record_id = delete_box2.get()
        c.execute('''
        update METHODS
        set METHOD = :Method
        ,AVG_i = :Interest_rate
        ,RISK_F = :Risk_fact
        where ID = :ID
        ''',
        {
        'Method': meth_name_editor.get(),
        'Interest_rate': interest_rate_editor.get(),
        'Risk_fact': risk_fact_editor.get(),
        'ID': record_id
        }
         )
        
        #commit and close
        conn.commit()
        conn.close

        editor.destroy()

    #create edit window   
    def window_edit_meth():
        global editor
        editor = Tk()
        editor.title('Update a Record')
        editor.geometry("400x400")

        #create global variables
        global meth_name_editor
        global interest_rate_editor
        global risk_fact_editor
        
        #create text boxes
        meth_name_editor = Entry(editor, width=30)
        meth_name_editor.grid(row=0, column = 1, padx=20, pady=(10,0))

        interest_rate_editor = Entry(editor, width=30)
        interest_rate_editor.grid(row=1, column = 1)

        risk_fact_editor = Entry(editor, width=30)
        risk_fact_editor.grid(row=2, column = 1)

        
        #create text box labels
        meth_name_label = Label(editor, text = "Method Description")
        meth_name_label.grid(row = 0, column = 0, pady=(10,0))

        interest_rate_label = Label(editor, text = "Average Interest Rate")
        interest_rate_label.grid(row = 1, column = 0)

        risk_fact_label = Label(editor, text = "Risk Factor")
        risk_fact_label.grid(row = 2, column = 0)

        #create db connection
        conn = sqlite3.connect(database)
        c = conn.cursor()

        record_id = delete_box2.get()
        #qry db
        c.execute('''
        select METHOD, AVG_i, RISK_F from METHODS where ID = ''' + record_id)
        records = c.fetchall()
        #loop thru results
        for record in records:
            meth_name_editor.insert(0,record[0])
            interest_rate_editor.insert(0,record[1])
            risk_fact_editor.insert(0,record[2])
       
        
        #commit and close
        conn.commit()
        conn.close

        #create save button
        save_btn = Button(editor, text="Save Record",command=edit_meth)
        save_btn.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx=143)



    #create function to delete a record
    def delete_meth():
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute("delete from METHODS where ID = " + delete_box2.get())

        #clear text boxes
        delete_box2.delete(0,END)

        #commit and close
        conn.commit()
        conn.close

        
    #create view function
    def view_meth():
        # Datebases
        conn = sqlite3.connect(database)
        c = conn.cursor()
        
        #reset auto increment
        c.execute('''
        UPDATE sqlite_sequence SET SEQ=0 WHERE NAME="METHODS";
        ''')
        
        c.execute('''
        select ID,METHOD, AVG_i, RISK_F from METHODS order by RISK_F
        ''')
        records = c.fetchall()
        print(tabulate(list(records),headers=["ID","Method"," Avg Interest","Risk Factor"]))
        
        #commit and close
        conn.commit()
        conn.close

    #create view portfolio function
    def view_port():
        # Datebases
        conn = sqlite3.connect(database)
        c = conn.cursor()


        #update min and max term years
        c.execute('''
        update TERM
        set MIN_TERM = :Min_Term
        ,MAX_TERM = :Max_Term
        ''',
        {
        'Min_Term': min_risk_year_box.get(),
        'Max_Term': max_risk_year_box.get()
        }
         )

        c.execute('''
        select a.end as [Years to], a.start as [Maturity], b.method ,a.Alloc*100 as Allocation, a.AVG_i as Avg_Int
        from R3 as a
        inner join Methods  as b
        on a.meth_id = b.id
        order by a.count desc, a.AVG_i
        ''')
        records = c.fetchall()
        print(tabulate(list(records),headers=["[Years to ","Maturity]","Method","% Allocation","Avg Interest"]))
        
        #commit and close
        conn.commit()
        conn.close

    #DISPLAY#

    #view button
    query_btn = Button(tab1, text="Show records",command=view_meth)
    query_btn.grid(row = 0, column = 0)
    #query_btn.grid(row = 0, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx=100)

    #create submit button
    submit_btn = Button(tab1, text = "Add record to database", command=window_add_meth)
    submit_btn.grid(row = 1, column = 0)

    #ID Field
    delete_box_label = Label(tab1, text = "Select ID")
    delete_box_label.grid(row=2, column=0)

    delete_box2 = Entry(tab1, width=10)
    delete_box2.grid(row=2, column=1)

    #create delete button
    delete_btn = Button(tab1, text="Delete Record",command=delete_meth)
    delete_btn.grid(row = 3, column = 0)

    #create update button
    edit_btn = Button(tab1, text="Edit Record",command=window_edit_meth)
    edit_btn.grid(row = 4, column = 0)

    #Max and Min Years to set linear iterpolation of risk factors
    max_risk_year_label = Label(tab1, text = "Years Out For 100% Max Risk Factor")
    max_risk_year_label.grid(row=5, column=0)

    max_risk_year_box = Entry(tab1, width=10)
    max_risk_year_box.grid(row=5, column=1)

    min_risk_year_label = Label(tab1, text = "Years Out For 100% Min Risk Factor")
    min_risk_year_label.grid(row=6, column=0)

    min_risk_year_box = Entry(tab1, width=10)
    min_risk_year_box.grid(row=6, column=1)

    #create db connection
    conn = sqlite3.connect(database)
    c = conn.cursor()

    #qry db
    c.execute('''
    select MAX_TERM, MIN_TERM from TERM''')
    records = c.fetchall()
    #loop thru results
    for record in records:
        max_risk_year_box.insert(0,record[0])
        min_risk_year_box.insert(0,record[1])

    #view profile button
    edit_btn = Button(tab1, text="View Risk Profile",command=view_port)
    edit_btn.grid(row = 7, column = 0)


    ################____CALCULATE TAB_____#####################

    def calc_results():
        #create db connection
        conn = sqlite3.connect(database)
        c = conn.cursor()

        #update min and max term years
        c.execute('''
        update TERM
        set MIN_TERM = :Min_Term
        ,MAX_TERM = :Max_Term
        ''',
        {
        'Min_Term': min_risk_year_box.get(),
        'Max_Term': max_risk_year_box.get()
        }
         )

        #update pricipal
        c.execute('''
        update P_INPUT
        set P_INPUT = :Principal
        ''',
        {
        'Principal': Initial_Amt_box.get()
        }
         )
        
        #commit and close
        conn.commit()
        conn.close

        
    ################## BEGINNING OF MAIN ALGORITYM ###########################
        #import sqlite3
        #from tabulate import tabulate

        def _power(x,y):
            r = pow(x,y)
            return r

        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        sqliteConnection.create_function("power",2,_power)

        print("Running...")

        Clear = '''
        update ITEMS
        set
        P = 0,
        P_CALC = 0,
        A_MIN = 0,
        A_MAX = 0,
        A_INT = 0,
        A_CALC = 0,
        F_CALC = 0,
        F_DIFF = 0;
        '''

        Clear2 = '''
        delete from Results;
        '''

        Insert ='''
        insert into RESULTS (cnt,ITEM_ID,N,I,Alloc,Meth_ID,start,end,ncnt,F_PCALC)
        select *
        from R4;
        '''

        cursor.execute(Clear)
        cursor.execute(Clear2)
        cursor.execute(Insert)
        sqliteConnection.commit()


        #Begin loop to determine max Pcalc (use ncnt in results to back calculate a P with no A and known F)
        F_loop3 ='''
        Select max(CNT) from RESULTS;
        '''

        cursor.execute(F_loop3)
        Max_Cnt = cursor.fetchone()[0]

        F_loop3 ='''
        Update P_INPUT
        set P_INT = P_INPUT;
        '''
        cursor.execute(F_loop3)
        sqliteConnection.commit()


        i = int(1)
        while (i <= Max_Cnt):

            F_loop4 ='''
            with get as(
            select max(nCNT)-(? -1) as nCNT, A.ITEM_ID 
            from Results as A
            group by ITEM_ID
            having max(nCNT)-(? -1) >= 0
            )

            , get2 as(
            Select A.nCNT, A.ITEM_ID, Meth_ID, F_PCALC*Alloc as F, N, I/100 as I
            from Results as A
            inner join get as B
            on a.nCNT = b.nCNT
            and a.ITEM_ID = B.ITEM_ID
            group by A.nCNT, A.ITEM_ID, Meth_ID
            )

            Update RESULTS 
            Set P =  
            round((select sum(B.F/(power((1+B.I),B.N))) AS P
            from RESULTS as A
            inner join get2 as B
            on a.nCNT = b.nCNT
            and a.ITEM_ID = B.ITEM_ID
            and a.Meth_ID = B.Meth_ID
            where A.nCNT = RESULTS.nCNT and A.ITEM_ID = RESULTS.ITEM_ID --and A.Meth_ID = RESULTS.Meth_ID
            group by A.nCNT, A.ITEM_ID),0)
            where exists(select * from get2 where nCNT = RESULTS.nCNT and ITEM_ID = RESULTS.ITEM_ID and Meth_ID = RESULTS.Meth_ID); 
            '''

            F_loop45 ='''
            with get as(
            select max(nCNT)-(? -1) as nCNT, A.ITEM_ID
            from Results as A
            group by ITEM_ID
            having max(nCNT)-(? -1) > 0)
                
            ,get2 as(
            select distinct A.ITEM_ID, A.nCNT, A.P
            from RESULTS as A
            inner join get as B
            on A.ITEM_ID = B.ITEM_ID
            and A.nCNT = B.nCNT
            )
                
            UPDATE RESULTS
            set F_PCALC = (
            select A.P 
            from get2 as A 
            where RESULTS.ITEM_ID = A.ITEM_ID and RESULTS.nCNT = A.nCNT - 1)
            where exists(Select * from get where ITEM_ID = RESULTS.ITEM_ID and nCNT - 1 = RESULTS.nCNT);
            '''
                
            cursor.execute(F_loop4,(i,i))
            cursor.execute(F_loop45,(i,i))
            sqliteConnection.commit()
            #print(i)
            i = i + 1


        F_loop5 = '''
        with get as(
        select min(nCNT) as nCNT, A.ITEM_ID 
        from Results as A
        --where Run = 1 
        group by ITEM_ID
        )

        UPDATE ITEMS
        set P_CALC = (
        select A.P
        from RESULTS as A 
        inner join get as B on 
        A.nCNT = b.nCNT
        and A.ITEM_ID = B.ITEM_ID
        where ITEMS.ID = A.ITEM_ID)
        where exists(Select * from get where ITEM_ID = ITEMS.ID);  
        ''' 

        cursor.execute(F_loop5)
        sqliteConnection.commit()

         
        #loop to distribute P amoungst the shortest N (terms)

        lcnt = int(1)
        pcnt = int(1)

        while (lcnt != 0 and pcnt != 0):

            F_loop5 = '''
            update items
            set FLG = 0;
            '''
            
            cursor.execute(F_loop5)

            if post_retire1 == 0:
                
                F_loop5 = '''
                with prep1 as (
                select min(a.term) as term
                from ITEMS as a
                where a.P = 0 and a.P_CALC <> 0
                )
                
                ,prep2 as (
                select max(ID) as ID
                from items as a
                inner join prep1 as b
                on a.term = b.term
                where a.P = 0 and a.P_CALC <> 0)
                
                ,prep3 as (
                select a.ID, a.P_CALC
                from ITEMS as a
                inner join prep2 as b
                on a.ID = b.ID)

                Update ITEMS
                set P = 
                (
                select case when b.P_INT > a.P_CALC then a.P_CALC else b.P_INT end as P
                --b.P_INT as P
                from prep3 as a
                inner join ITEMS as c
                on a.ID = c.ID
                cross join P_INPUT as b
                where a.ID = ITEMS.ID)
                ,FLG = (select 1
                from prep3 as a
                where a.ID = ITEMS.ID)
                where exists (select ID from prep2 where ID = ITEMS.ID);
                '''

            else:
                ##MODIFIED UPDATE QRY BELOW FOR POST RETIREMENT
                
                F_loop5 = '''
                with prep1 as (
                select min(a.term) as term
                from ITEMS as a
                where a.P = 0 and a.P_CALC <> 0
                )
                
                ,prep2 as (
                select max(ID) as ID
                from items as a
                inner join prep1 as b
                on a.term = b.term
                where a.P = 0 and a.P_CALC <> 0)
                
                ,prep3 as (
                select a.ID, a.P_CALC
                from ITEMS as a
                inner join prep2 as b
                on a.ID = b.ID)

                Update ITEMS
                set P = 
                (
                select b.P_INT as P
                from prep3 as a
                inner join ITEMS as c
                on a.ID = c.ID
                cross join P_INPUT as b
                where a.ID = ITEMS.ID)
                ,FLG = (select 1
                from prep3 as a
                where a.ID = ITEMS.ID)
                where exists (select ID from prep2 where ID = ITEMS.ID);
                '''
            #end of if else
            
            cursor.execute(F_loop5)

            F_loop5 = ''' 
            update P_INPUT
            set P_INT = (select a.P_INT - b.P
            from P_INPUT as a
            cross join ITEMS as b
            where b.FLG = 1);
            '''

            cursor.execute(F_loop5)


            F_loop5 = '''
            select count(ID) from ITEMS where P = 0 and P_CALC <> 0;
            '''
            cursor.execute(F_loop5)
            lcnt = cursor.fetchone()[0]

            F_loop5 = '''
            select P_INT from P_INPUT;
            '''
            cursor.execute(F_loop5)
            pcnt = cursor.fetchone()[0]
        #end of loop


        if post_retire1 == 0:

            A_Min_Upt ='''
            ;with stg as(
            select A.ITEM_ID, max(A.avg_i) as MAX_i, min(A.avg_i) as MIN_i
            from R4 as A
            group by A.ITEM_ID
            )

            update ITEMS
            set A_MIN = round((select A.MAX_i/100 * (ITEMS.F_GOAL - ITEMS.P * power((1+A.MAX_i/100),ITEMS.TERM)) * 1 / (power((1+A.MAX_i/100),ITEMS.TERM) - 1)
            From stg AS A
            WHERE ITEMS.ID = A.ITEM_ID),2)
            WHERE ITEMS.ID IN (select ITEM_ID From stg);
            '''

            A_Max_Upt ='''
            ;with stg as(
            select A.ITEM_ID, max(A.avg_i) as MAX_i, min(A.avg_i) as MIN_i
            from R4 as A
            group by A.ITEM_ID
            )

            update ITEMS
            set A_MAX = round((select A.MIN_i/100 * (ITEMS.F_GOAL - ITEMS.P * power((1+A.MIN_i/100),ITEMS.TERM)) * 1 / (power((1+A.MIN_i/100),ITEMS.TERM) - 1)
            From stg AS A
            WHERE ITEMS.ID = A.ITEM_ID),2)
            WHERE ITEMS.ID IN (select ITEM_ID From stg);
            '''

            A_Int_Upt ='''
            update ITEMS
            set A_INT = round(0.025*(A_MAX-A_MIN),2),
            A_CALC = A_MIN,
            --A_CALC = round(A_MIN,0),
            F_CALC = P,
            F_DIFF = case when F_GOAL*1 > P*1 then round(F_GOAL - P,0) else round(P - F_GOAL,0) end;
            '''

        else:
            
            ##MODIFIED UPDATE MIN_A and MAX_A QRYS BELOW FOR POST RETIREMENT

            A_Min_Upt ='''
            ;with stg as(
            select A.ITEM_ID, max(A.avg_i) as MAX_i, min(A.avg_i) as MIN_i
            from R4 as A
            group by A.ITEM_ID
            )

            update ITEMS
            set A_MAX = round((select A.MAX_i/100 * (ITEMS.F_GOAL - ITEMS.P * power((1+A.MAX_i/100),ITEMS.TERM)) * 1 / (power((1+A.MAX_i/100),ITEMS.TERM) - 1) 
            From stg AS A
            WHERE ITEMS.ID = A.ITEM_ID),2)
            WHERE ITEMS.ID IN (select ITEM_ID From stg);
            '''

            A_Max_Upt ='''
            ;with stg as(
            select A.ITEM_ID, max(A.avg_i) as MAX_i, min(A.avg_i) as MIN_i
            from R4 as A
            group by A.ITEM_ID
            )

            update ITEMS
            set A_MIN = round((select A.MIN_i/100 * (ITEMS.F_GOAL - ITEMS.P * power((1+A.MIN_i/100),ITEMS.TERM)) * 1 / (power((1+A.MIN_i/100),ITEMS.TERM) - 1)
            From stg AS A
            WHERE ITEMS.ID = A.ITEM_ID),2)
            WHERE ITEMS.ID IN (select ITEM_ID From stg);
            '''

            A_Int_Upt ='''
            update ITEMS
            set A_INT = round(0.025*(A_MAX-A_MIN),2),
            A_CALC = A_MIN,
            --A_CALC = round(A_MIN,0),
            F_CALC = P,
            F_DIFF = case when F_GOAL*1 > P*1 then round(F_GOAL - P,0) else round(P - F_GOAL,0) end;
            '''
        #end of if else

        cursor.execute(A_Min_Upt)
        cursor.execute(A_Max_Upt)
        cursor.execute(A_Int_Upt)
        sqliteConnection.commit()


        #begin if statement and loop for F_Diff > 0

        lcnt = int(1)
        t=1 #t constraint in the next line just needs to be greater than the number of A_int determined.
        #There are currently 40 A_Int determined in the qry above. This t variable is just here
        # to prevent indefinite looping if the F_DIFF never gets below 0.
        while (lcnt > 0 and t < 45):

            F_loop0 ='''
            update RESULTS
            set Run = 0;
            '''

            F_loop1 ='''
            update RESULTS
            set A = (select A_CALC from ITEMS where ID = RESULTS.ITEM_ID)
            ,P = (select P from ITEMS where ID = RESULTS.ITEM_ID)
            ,RUN = 1
            where exists(select * from ITEMS where ID = RESULTS.ITEM_ID and F_DIFF>0);
            '''

            F_loop3 ='''
            Select max(CNT) from RESULTS WHERE RUN = 1;
            '''

            cursor.execute(F_loop0)
            cursor.execute(F_loop1)
            sqliteConnection.commit()
            cursor.execute(F_loop3)
            Max_Cnt = cursor.fetchone()[0]

            i = int(1)
            while (i <= Max_Cnt):

                F_loop4 ='''
                with get as(
                select max(CNT)-(? -1) as CNT, A.ITEM_ID 
                from Results as A
                where Run = 1
                group by ITEM_ID
                having max(CNT)-(? -1) > 0)

                , get2 as(
                Select A.CNT, A.ITEM_ID, Meth_ID, P*Alloc as P, A*Alloc as A, N, I/100 as I
                from Results as A
                inner join get as B
                on a.CNT = b.CNT
                and a.ITEM_ID = B.ITEM_ID
                group by A.CNT, A.ITEM_ID, Meth_ID)

                Update RESULTS 
                Set F_CALC =  
                round((select B.P*(power(1+B.I,B.N))+B.A/B.I*(power(1+B.I,B.N)-1) AS F
                from RESULTS as A
                inner join get2 as B
                on a.CNT = b.CNT
                and a.ITEM_ID = B.ITEM_ID
                and a.Meth_ID = B.Meth_ID
                where A.CNT = RESULTS.CNT and A.ITEM_ID = RESULTS.ITEM_ID and A.Meth_ID = RESULTS.Meth_ID
                --group by A.CNT, A.ITEM_ID
                ),0)
                where exists(select * from get2 where CNT = RESULTS.CNT and ITEM_ID = RESULTS.ITEM_ID and Meth_ID = RESULTS.Meth_ID); 
                '''

                F_loop45 ='''
                with get as(
                select max(CNT)-(? -1) as CNT, A.ITEM_ID
                from Results as A
                where Run = 1
                group by ITEM_ID
                having max(CNT)-(? -1) > 0)
                
                ,get2 as(
                select A.ITEM_ID, A.CNT, sum(A.F_CALC) as F_CALC
                from RESULTS as A
                inner join get as B
                on A.ITEM_ID = B.ITEM_ID
                and A.CNT = B.CNT
                group by A.ITEM_ID, A.CNT)
                
                UPDATE RESULTS
                set P = (
                select A.F_CALC as P 
                from get2 as A 
                where RESULTS.ITEM_ID = A.ITEM_ID and RESULTS.CNT = A.CNT - 1)
                where exists(Select * from get where ITEM_ID = RESULTS.ITEM_ID and CNT - 1 = RESULTS.CNT);
                '''
                
                cursor.execute(F_loop4,(i,i))
                cursor.execute(F_loop45,(i,i))
                sqliteConnection.commit()
                #print(i)
                i = i + 1

            F_loop5 = '''
            with get as(
            select min(CNT) as CNT, A.ITEM_ID 
            from Results as A
            where Run = 1 
            group by ITEM_ID
            )


            UPDATE ITEMS
            set F_CALC = (
            select sum(A.F_CALC) as F_CALC 
            from RESULTS as A 
            inner join get as B on 
            A.CNT = b.CNT
            and A.ITEM_ID = B.ITEM_ID
            where ITEMS.ID = A.ITEM_ID
            group by A.ITEM_ID, A.CNT)
            where exists(Select * from get where ITEM_ID = ITEMS.ID);  
            ''' 

            cursor.execute(F_loop5)
            sqliteConnection.commit()

            F_loop6 = '''
            Update ITEMS
            set F_DIFF = case when F_GOAL > P then round(F_GOAL - F_CALC,0) else round(F_CALC - F_GOAL,0) end;
            '''
          
            cursor.execute(F_loop6)
            sqliteConnection.commit()

            F_loop7 = '''
            update ITEMS
            set A_CALC = A_CALC + A_INT
            --set A_CALC = round(A_CALC + A_INT,0)
            where F_DIFF > 0;
            '''

            cursor.execute(F_loop7)
            sqliteConnection.commit()

            F_loop8 ='''
            select count(F_DIFF) from ITEMS where F_DIFF > 0;
            '''

            cursor.execute(F_loop8)
            #print ("A", lcnt," ",t)
            t = t + 1
            lcnt = cursor.fetchone()[0]
            

        #End loop of if statement


        ############RESULTS###################
        #update nstart and nend date
        F_loop66 ='''
        with prep as (
            select A.Item_ID, max(end) as max_end
            from RESULTS as a
            group by A.item_id
            --order by 2,1
            )
            
        ,prep2 as (
            select A.Item_ID, A.CNT, b.max_end
            from RESULTS as a
            inner join prep as b
            on a.ITEM_ID = b.ITEM_ID
            group by A.item_id, A.CNT
            --order by 2,1
            )


        update RESULTS
        set nstart = 
        (select (a.end - b.max_end)*(-1) 
        from RESULTS  as a
        inner join prep2 as b
        on a.ITEM_ID = b.ITEM_ID
        and a.CNT = b.CNT
        where A.CNT = RESULTS.CNT and A.ITEM_ID = RESULTS.ITEM_ID)
        ,nend= 
        (select (a.start - b.max_end)*(-1) 
        from RESULTS  as a
        inner join prep2 as b
        on a.ITEM_ID = b.ITEM_ID
        and a.CNT = b.CNT
        where A.CNT = RESULTS.CNT and A.ITEM_ID = RESULTS.ITEM_ID)
        where exists(select * from prep2 where CNT= RESULTS.CNT and ITEM_ID = RESULTS.ITEM_ID)
        '''
        cursor.execute(F_loop66)

        F_loop65 ='''
        select count(ID) from ITEMS;
        '''
        cursor.execute(F_loop65)
        lcnt = cursor.fetchone()[0]

        print ("RESULTS BY ITEM:")
        i = int(1)
        while i <= lcnt:

            Item_Name ='''
            with prep as (
            select max(ID) as ID 
            from ITEMS
            where ID in (select ID from ITEMS order by ID limit ?)
            )
            
            select Item
            from ITEMS as a
            inner join prep as b
            on a.ID = b.ID
            '''
            
            Results_3 ='''
            with prep as (
            select max(ID) as ID 
            from ITEMS
            where ID in (select ID from ITEMS order by ID limit ?)
            )
                
        select 
             c.nstart as START
            ,c.nend as END
            ,d.METHOD
            ,c.I as INTEREST
            ,round(c.alloc*100) as PERCENT_ALLOCATION
            ,round(c.P*c.Alloc,0) as INITIAL_AMT
            ,round(c.A*c.Alloc,0) as ANNUAL_AMT
            ,round(c.F_Calc,0) as FUTURE_AMT
            from RESULTS as c
            inner join METHODS as d
            on C.Meth_ID= D.ID
            inner join prep as e
            on C.Item_ID= E.ID
        order by C.item_id, C.start desc, C.Meth_ID
            '''

            cursor.execute(Item_Name,(i,))
            record = cursor.fetchall()
            print(tabulate(list(record),headers=()))
            cursor.execute(Results_3,(i,))
            record = cursor.fetchall()
            print(tabulate(list(record),headers=["Starting Year","Ending Year","Method","% Interest Rate","% Allocation","Starting Amt","Annual Amt","Ending Amt"]))
            i = i + 1

        
        print ("Recommended amount/allocation to invest this year:")

        Results_1 ='''
            with prep as (
            select ITEM_ID, max(CNT) as CNT
            from RESULTS
            group by ITEM_ID)

            ,prep2 as(
            select a.METH_ID, P*Alloc as P, A*Alloc as A
            from RESULTS as a
            inner join prep as b
            on a.CNT = b.CNT
            and a.ITEM_ID = b.ITEM_ID)

            ,prep3 as (
            select a.METHOD, round(sum(b.P),0) as INITIAL, round(sum(b.A),0) as ANNUAL
            from METHODS as a
            inner join prep2 as b
            on a.ID = b.METH_ID
            group by a.ID)

            select * from prep3
            union all
            select 'TOTAL:', sum(INITIAL), sum(ANNUAL)
            from prep3;
            '''
                
        cursor.execute(Results_1)
        record = cursor.fetchall()
        print(tabulate(list(record),headers=["Method","Initial Investment","Annual Investment"]))


        """
        print ("RESULTS BY YEAR:")

        F_loop3='''
        Select max(CNT) from RESULTS
        --Select 1
        '''

        cursor.execute(F_loop3)
        Max_Cnt = cursor.fetchone()[0]

        i = int(1)
        while i <= Max_Cnt:

            Results_0 ='''
            select nstart, nend
            from RESULTS
            where ncnt = (?-1)
            group by ncnt
            '''

            Results_1 ='''
            with prep as (
            select ITEM_ID, max(CNT) -(?-1) as CNT
            from RESULTS
            group by ITEM_ID)

            ,prep2 as(
            select a.METH_ID, P*Alloc as P, A*Alloc as A
            from RESULTS as a
            inner join prep as b
            on a.CNT = b.CNT
            and a.ITEM_ID = b.ITEM_ID)

            ,prep3 as (
            select a.METHOD, round(sum(b.P),0) as INITIAL, round(sum(b.A),0) as ANNUAL
            from METHODS as a
            inner join prep2 as b
            on a.ID = b.METH_ID
            group by a.ID)

            select * from prep3
            union all
            select 'TOTAL:', sum(INITIAL), sum(ANNUAL)
            from prep3;
            '''
                
            cursor.execute(Results_0,(i,))
            record = cursor.fetchall()
            print(tabulate(list(record),headers=["Start Year","End Year"]))
            cursor.execute(Results_1,(i,))
            record = cursor.fetchall()
            print(tabulate(list(record),headers=["Method","Initial Investment","Annual Investment"]))
            i = i + 1
        """

        cursor.close()

    ################## END OF MAIN ALGORITHYM ############################


    #DISPLAY

    #Principal 
    Initial_Amt_label = Label(tab3, text = "Current Principal")
    Initial_Amt_label.grid(row=0, column=0)

    Initial_Amt_box = Entry(tab3, width=10)
    Initial_Amt_box.grid(row=0, column=1)

    #create db connection
    conn = sqlite3.connect(database)
    c = conn.cursor()

    #qry db
    c.execute('''
    select P_INPUT FROM P_INPUT''')
    records = c.fetchall()
    #loop thru results
    for record in records:
        Initial_Amt_box.insert(0,record[0])

    #Calculate button
    query_btn = Button(tab3, text="Calculate Results",command=calc_results)
    query_btn.grid(row = 3, column = 0)


    conn.commit()
    conn.close
    root.mainloop()



#create save button
start_btn = Button(start, text="Lets Go!",command=lets_go)
start_btn.grid(row = 3, column = 0, columnspan = 2, pady = 10, padx = 10, ipadx=143)

start.mainloop()

