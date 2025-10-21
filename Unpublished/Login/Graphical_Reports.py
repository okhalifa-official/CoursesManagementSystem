
        # ==========================
        # Chart 1: Financial Overview (Stacked)
        # ==========================
        fig1, ax1 = plt.subplots(figsize=(7, 5))
        x = np.arange(len(courses))
        width = 0.6
        ax1.bar(x, paid, width, label='Paid', color='#4CAF50')
        ax1.bar(x, remaining, width, bottom=paid, label='Remaining', color='#E57373')

        # Annotate percentages
        for i, (p, e) in enumerate(zip(paid, expected)):
            ax1.text(i, p / 2, f"{p/e*100:.1f}%", ha='center', va='center', color='white', fontsize=10, weight='bold')

        ax1.set_xticks(x)
        ax1.set_xticklabels(courses)
        ax1.set_ylabel('Amount (EGP)')
        ax1.set_title(f'Financial Breakdown per Course\nTotal Revenue: {total_revenue:,} EGP | Expected: {total_expected:,} EGP')
        ax1.legend()
        ax1.grid(True, axis='y', linestyle='--', alpha=0.6)
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Financial Breakdown")
        add_chart(tab1, fig1)

        # ==========================
        # Chart 2: Payment Efficiency (Expected vs Paid with trend)
        # ==========================
        fig2, ax2 = plt.subplots(figsize=(7, 5))
        ax2.bar(x - 0.2, expected, width/2, label='Expected', color='#64B5F6')
        ax2.bar(x + 0.2, paid, width/2, label='Paid', color='#81C784')
        ax2.plot(x, paid_ratio, color='#F57C00', marker='o', linestyle='--', label='% Paid')

        # Add line labels
        for i, pct in enumerate(paid_ratio):
            ax2.text(i, max(paid[i], expected[i]) + 500, f"{pct}%", ha='center', color='#F57C00', fontsize=9)

        ax2.set_xticks(x)
        ax2.set_xticklabels(courses)
        ax2.set_ylabel('Amount (EGP)')
        ax2.set_title(f'Payment Efficiency per Course (Average Paid: {avg_paid:,.0f} EGP, Expected: {avg_expected:,.0f} EGP)')
        ax2.legend()
        ax2.grid(True, axis='y', linestyle='--', alpha=0.6)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Payment Efficiency")
        add_chart(tab2, fig2)

        # ==========================
        # Chart 3: Enrollment & Financial Correlation
        # ==========================
        fig3, ax3 = plt.subplots(figsize=(7, 5))
        ax3.bar(courses, enrolled, color='#FFD54F', label='Enrolled Students')
        ax3_2 = ax3.twinx()
        ax3_2.plot(courses, paid_ratio, color='#388E3C', marker='o', label='% Paid')

        ax3.set_ylabel('Students')
        ax3_2.set_ylabel('% Paid')
        ax3.set_title('Enrollment vs Payment Completion Rate')
        ax3.grid(True, axis='y', linestyle='--', alpha=0.6)

        # Combine legends from both axes
        lines, labels = ax3.get_legend_handles_labels()
        lines2, labels2 = ax3_2.get_legend_handles_labels()
        ax3_2.legend(lines + lines2, labels + labels2, loc='upper left')

        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Enrollment & Payments")
        add_chart(tab3, fig3)

        # ==========================
        # Chart 4: Payment Distribution (Pie Chart)
        # ==========================
        fig4, ax4 = plt.subplots(figsize=(6, 5))
        total_paid_sum = np.sum(paid)
        total_remaining_sum = np.sum(remaining)

        ax4.pie(
            [total_paid_sum, total_remaining_sum],
            labels=[f'Paid ({total_paid_sum:,.0f} EGP)', f'Remaining ({total_remaining_sum:,.0f} EGP)'],
            autopct='%1.1f%%',
            colors=['#81C784', '#E57373'],
            startangle=90,
            textprops={'fontsize': 11}
        )
        ax4.set_title('Overall Payment Distribution')
        ax4.axis('equal')

        tab4_pie = ttk.Frame(notebook)
        notebook.add(tab4_pie, text="Payment Distribution")
        add_chart(tab4_pie, fig4)


        # ==========================
        # Chart 5: Revenue vs Enrollment Correlation (Scatter)
        # ==========================
        fig5, ax5 = plt.subplots(figsize=(7, 5))
        scatter = ax5.scatter(
            enrolled, paid, c=paid_ratio, cmap='viridis', s=120, edgecolors='k'
        )

        ax5.set_xlabel('Enrolled Students')
        ax5.set_ylabel('Total Paid (EGP)')
        ax5.set_title('Revenue vs Enrollment Correlation')
        ax5.grid(True, linestyle='--', alpha=0.6)

        # Annotate each point with course name
        for i, name in enumerate(courses):
            ax5.text(enrolled[i] + 0.1, paid[i] + 200, name, fontsize=9, alpha=0.8)

        # Color bar to indicate payment ratio
        cbar = plt.colorbar(scatter, ax=ax5)
        cbar.set_label('% Paid')

        tab5 = ttk.Frame(notebook)
        notebook.add(tab5, text="Revenue Correlation")
        add_chart(tab5, fig5)


        # ==========================
        # Chart 6: Course Comparison Radar Chart
        # ==========================
        from math import pi

        metrics = ['Paid %', 'Remaining %', 'Enrollment %', 'Expected %']
        num_vars = len(metrics)

        # Normalize data to percentage scale
        max_enrolled = max(enrolled)
        enrolled_pct = (enrolled / max_enrolled) * 100
        remaining_pct = (remaining / expected) * 100
        expected_pct = (expected / np.max(expected)) * 100

        # Create radar chart
        fig6 = plt.figure(figsize=(7, 6))
        ax6 = fig6.add_subplot(111, polar=True)

        angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
        angles += angles[:1]  # close the loop

        for i, course in enumerate(courses):
            values = [paid_ratio[i], remaining_pct[i], enrolled_pct[i], expected_pct[i]]
            values += values[:1]
            ax6.plot(angles, values, linewidth=1.5, linestyle='solid', label=course)
            ax6.fill(angles, values, alpha=0.1)

        ax6.set_xticks(angles[:-1])
        ax6.set_xticklabels(metrics)
        ax6.set_title("Course Performance Radar Comparison")
        ax6.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
        tab6 = ttk.Frame(notebook)
        notebook.add(tab6, text="Radar Comparison")
        add_chart(tab6, fig6)


	# ==========================
        # Export Button
        # ==========================
        def export_current_tab():
            """Export the chart from the current notebook tab as a PNG image."""
            tab_name = notebook.tab(notebook.select(), "text")
            if tab_name not in self.figures:
                messagebox.showinfo("Export Unavailable", f"No exportable chart in '{tab_name}' tab.")
                return

            fig = self.figures[tab_name]
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg"), ("All Files", "*.*")],
                initialfile=f"{tab_name.replace(' ', '_')}.png"
            )
            if file_path:
                try:
                    fig.savefig(file_path, dpi=300, bbox_inches='tight')
                    messagebox.showinfo("Export Successful", f"Chart saved as:\n{os.path.basename(file_path)}")
                except Exception as e:
                    messagebox.showerror("Export Failed", f"An error occurred:\n{e}")

        export_btn = ttk.Button(self.visuals_frame, text="📊 Export Current Chart", command=export_current_tab)
        export_btn.pack(side="bottom", pady=10)
