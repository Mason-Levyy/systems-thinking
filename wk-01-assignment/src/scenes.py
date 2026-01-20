"""
Manim Scenes for Coffee Shop System Visualization
Demonstrates stocks, flows, and feedback loops using mathematical animations.
"""
from manim import *


class StocksScene(Scene):
    """Visualizes the four main stocks in a coffee shop system."""
    
    def construct(self):
        # Title
        title = Text("Coffee Shop Stocks", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Stock data
        stocks = [
            ("Inventory\nLevels", 0.7, "#4CAF50"),
            ("Order\nQueue", 0.4, "#FF9800"),
            ("Cash\nReserves", 0.85, "#2196F3"),
            ("Customer\nDensity", 0.55, "#9C27B0")
        ]
        
        # Create stock visualizations
        stock_group = VGroup()
        
        for i, (name, level, color) in enumerate(stocks):
            # Container
            container = Rectangle(width=1.5, height=3, color=WHITE, stroke_width=2)
            
            # Fill level
            fill_height = level * 2.8
            fill = Rectangle(
                width=1.4, 
                height=fill_height, 
                fill_color=color,
                fill_opacity=0.8,
                stroke_width=0
            )
            fill.align_to(container, DOWN).shift(UP * 0.1)
            
            # Label
            label = Text(name, font_size=18, color=WHITE)
            label.next_to(container, DOWN, buff=0.3)
            
            # Percentage
            pct = Text(f"{int(level*100)}%", font_size=20, color=color)
            pct.next_to(container, UP, buff=0.1)
            
            stock_viz = VGroup(container, fill, label, pct)
            stock_group.add(stock_viz)
        
        stock_group.arrange(RIGHT, buff=1)
        stock_group.next_to(title, DOWN, buff=0.8)
        
        # Animate each stock appearing
        for stock in stock_group:
            self.play(FadeIn(stock), run_time=0.5)
        
        self.wait()
        
        # Animate level changes
        subtitle = Text("Stocks fluctuate based on inflows and outflows", 
                       font_size=24, color=GRAY)
        subtitle.to_edge(DOWN)
        self.play(Write(subtitle))
        
        self.wait(2)


class FlowsScene(Scene):
    """Visualizes the flows (inflows and outflows) in the coffee shop system."""
    
    def construct(self):
        # Title
        title = Text("Coffee Shop Flows", font_size=48, color=WHITE)
        title.to_edge(UP)
        self.play(Write(title))
        
        # Create central stock representation
        stock = RoundedRectangle(width=3, height=2, corner_radius=0.3, 
                                  fill_color="#333333", fill_opacity=0.8)
        stock_label = Text("STOCK", font_size=24, color=WHITE)
        stock_group = VGroup(stock, stock_label)
        
        # Inflows (left side)
        inflow_arrow = Arrow(LEFT * 4, LEFT * 1.7, buff=0, color="#4CAF50", stroke_width=6)
        inflow_label = Text("Inflow", font_size=20, color="#4CAF50")
        inflow_label.next_to(inflow_arrow, UP)
        
        # Outflows (right side)
        outflow_arrow = Arrow(RIGHT * 1.7, RIGHT * 4, buff=0, color="#F44336", stroke_width=6)
        outflow_label = Text("Outflow", font_size=20, color="#F44336")
        outflow_label.next_to(outflow_arrow, UP)
        
        self.play(Create(stock_group))
        self.play(GrowArrow(inflow_arrow), Write(inflow_label))
        self.play(GrowArrow(outflow_arrow), Write(outflow_label))
        
        self.wait()
        
        # Show specific flows
        flows_data = [
            ("Procurement", "inflow", "#4CAF50"),
            ("Order Placement", "inflow", "#4CAF50"),
            ("Sales/Consumption", "outflow", "#F44336"),
            ("Order Fulfillment", "outflow", "#F44336")
        ]
        
        flow_texts = VGroup()
        for i, (name, flow_type, color) in enumerate(flows_data):
            text = Text(f"• {name}", font_size=18, color=color)
            flow_texts.add(text)
        
        flow_texts.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        flow_texts.to_edge(DOWN, buff=1)
        
        self.play(FadeIn(flow_texts, shift=UP))
        
        # Animate particles flowing
        for _ in range(3):
            # Inflow particle
            in_particle = Dot(color="#4CAF50", radius=0.15)
            in_particle.move_to(LEFT * 5)
            
            # Outflow particle
            out_particle = Dot(color="#F44336", radius=0.15)
            out_particle.move_to(ORIGIN)
            
            self.play(
                in_particle.animate.move_to(ORIGIN),
                out_particle.animate.move_to(RIGHT * 5),
                run_time=0.8
            )
            self.remove(in_particle, out_particle)
        
        self.wait(2)


class FeedbackLoopsScene(Scene):
    """
    Combined visualization of both positive (reinforcing) and negative (balancing) feedback loops.
    Shows Word of Mouth loop first, then transitions to Wait Time Regulator loop.
    """
    
    def construct(self):
        # ========== POSITIVE LOOP (Word of Mouth) ==========
        title = Text("Feedback Loops", font_size=42, color=WHITE)
        title.to_edge(UP, buff=0.3)
        
        loop_type = Text("1. Reinforcing Loop (+)", font_size=28, color="#4CAF50")
        loop_name = Text("\"Word of Mouth\"", font_size=22, color=GRAY)
        header = VGroup(loop_type, loop_name).arrange(DOWN, buff=0.1)
        header.next_to(title, DOWN, buff=0.3)
        
        self.play(Write(title), FadeIn(header, shift=UP))
        
        # Positive loop components
        pos_components = [
            "High Quality",
            "Customer\nSatisfaction",
            "Positive\nReviews",
            "New\nCustomers",
            "Higher\nRevenue"
        ]
        
        # Create circular arrangement
        n = len(pos_components)
        radius = 1.8
        pos_boxes = VGroup()
        
        for i, comp in enumerate(pos_components):
            angle = PI/2 - (2 * PI * i / n)
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            pos[1] -= 0.5  # Shift down
            
            box = RoundedRectangle(width=1.8, height=1, corner_radius=0.15,
                                   fill_color="#1a1a2e", fill_opacity=0.9,
                                   stroke_color="#4CAF50", stroke_width=2)
            label = Text(comp, font_size=12, color=WHITE)
            group = VGroup(box, label)
            group.move_to(pos)
            pos_boxes.add(group)
        
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in pos_boxes], lag_ratio=0.12))
        
        # Create arrows between components
        pos_arrows = VGroup()
        for i in range(n):
            start = pos_boxes[i].get_center()
            end = pos_boxes[(i+1) % n].get_center()
            direction = end - start
            direction = direction / np.linalg.norm(direction)
            
            arrow = Arrow(
                start + direction * 0.75,
                end - direction * 0.75,
                color="#4CAF50",
                stroke_width=2.5,
                buff=0,
                max_tip_length_to_length_ratio=0.2
            )
            pos_arrows.add(arrow)
        
        self.play(LaggedStart(*[GrowArrow(a) for a in pos_arrows], lag_ratio=0.1))
        
        # Add reinforcing symbol
        plus = Text("+", font_size=40, color="#4CAF50", weight=BOLD)
        circle = Circle(radius=0.35, color="#4CAF50", stroke_width=2)
        pos_symbol = VGroup(circle, plus)
        pos_symbol.move_to(DOWN * 0.5)
        
        self.play(Create(pos_symbol))
        
        # Explanation
        pos_explain = Text("Growth compounds! Quality → Customers → Revenue → Better Quality", 
                          font_size=14, color=GRAY)
        pos_explain.to_edge(DOWN, buff=0.4)
        self.play(Write(pos_explain))
        
        self.wait(2)
        
        # ========== TRANSITION ==========
        # Fade out positive loop, fade in negative loop
        pos_elements = VGroup(pos_boxes, pos_arrows, pos_symbol, pos_explain, header)
        
        new_header = VGroup(
            Text("2. Balancing Loop (−)", font_size=28, color="#FF9800"),
            Text("\"Wait Time Regulator\"", font_size=22, color=GRAY)
        ).arrange(DOWN, buff=0.1)
        new_header.next_to(title, DOWN, buff=0.3)
        
        self.play(
            FadeOut(pos_elements, shift=LEFT * 2),
            FadeIn(new_header, shift=RIGHT * 2),
            run_time=0.8
        )
        
        # ========== NEGATIVE LOOP (Wait Time Regulator) ==========
        neg_components = [
            "High\nOrder Queue",
            "Long\nWait Times",
            "Customers\nLeave",
            "Queue\nShrinks"
        ]
        
        n2 = len(neg_components)
        neg_boxes = VGroup()
        
        for i, comp in enumerate(neg_components):
            angle = PI/2 - (2 * PI * i / n2)
            pos = radius * np.array([np.cos(angle), np.sin(angle), 0])
            pos[1] -= 0.5
            
            box = RoundedRectangle(width=1.8, height=1, corner_radius=0.15,
                                   fill_color="#1a1a2e", fill_opacity=0.9,
                                   stroke_color="#FF9800", stroke_width=2)
            label = Text(comp, font_size=12, color=WHITE)
            group = VGroup(box, label)
            group.move_to(pos)
            neg_boxes.add(group)
        
        self.play(LaggedStart(*[FadeIn(b, scale=0.8) for b in neg_boxes], lag_ratio=0.12))
        
        # Create arrows
        neg_arrows = VGroup()
        for i in range(n2):
            start = neg_boxes[i].get_center()
            end = neg_boxes[(i+1) % n2].get_center()
            direction = end - start
            direction = direction / np.linalg.norm(direction)
            
            arrow = Arrow(
                start + direction * 0.8,
                end - direction * 0.8,
                color="#FF9800",
                stroke_width=2.5,
                buff=0,
                max_tip_length_to_length_ratio=0.2
            )
            neg_arrows.add(arrow)
        
        self.play(LaggedStart(*[GrowArrow(a) for a in neg_arrows], lag_ratio=0.1))
        
        # Balancing symbol
        minus = Text("−", font_size=40, color="#FF9800", weight=BOLD)
        neg_circle = Circle(radius=0.35, color="#FF9800", stroke_width=2)
        neg_symbol = VGroup(neg_circle, minus)
        neg_symbol.move_to(DOWN * 0.5)
        
        self.play(Create(neg_symbol))
        
        # Equilibrium indicator
        eq_text = Text("System self-corrects! Long waits → Fewer customers → Queue shrinks", 
                      font_size=14, color=GRAY)
        eq_text.to_edge(DOWN, buff=0.4)
        self.play(Write(eq_text))
        
        self.wait(2)
        
        # ========== FINAL SUMMARY ==========
        neg_elements = VGroup(neg_boxes, neg_arrows, neg_symbol, eq_text, new_header)
        
        self.play(FadeOut(neg_elements))
        
        # Show both loops side by side (summary)
        summary_title = Text("Two Types of Feedback", font_size=28, color=WHITE)
        summary_title.next_to(title, DOWN, buff=0.4)
        
        # Left: Positive
        pos_summary = VGroup(
            Text("+", font_size=48, color="#4CAF50", weight=BOLD),
            Text("Reinforcing", font_size=20, color="#4CAF50"),
            Text("Amplifies change", font_size=14, color=GRAY),
            Text("(exponential growth/decline)", font_size=12, color=GRAY)
        ).arrange(DOWN, buff=0.15)
        
        # Right: Negative
        neg_summary = VGroup(
            Text("−", font_size=48, color="#FF9800", weight=BOLD),
            Text("Balancing", font_size=20, color="#FF9800"),
            Text("Resists change", font_size=14, color=GRAY),
            Text("(seeks equilibrium)", font_size=12, color=GRAY)
        ).arrange(DOWN, buff=0.15)
        
        summaries = VGroup(pos_summary, neg_summary).arrange(RIGHT, buff=2)
        summaries.move_to(ORIGIN).shift(DOWN * 0.3)
        
        self.play(Write(summary_title))
        self.play(FadeIn(pos_summary, shift=RIGHT), FadeIn(neg_summary, shift=LEFT))
        
        self.wait(3)


class FullSystemScene(Scene):
    """
    Clean top-down coffee shop simulation with prominent step labels.
    Simplified layout with clear customer flow visualization.
    """
    
    def construct(self):
        # ========== STEP INDICATOR (large, prominent at top) ==========
        step_bg = Rectangle(width=10, height=0.8, color="#333", 
                           fill_color="#222", fill_opacity=0.95, stroke_width=0)
        step_bg.to_edge(UP, buff=0.1)
        
        step_text = Text("", font_size=28, color="#FFD54F", weight=BOLD)
        step_text.move_to(step_bg)
        
        self.add(step_bg)
        
        # Helper to update step indicator
        def show_step(text, color="#FFD54F"):
            new_text = Text(text, font_size=28, color=color, weight=BOLD)
            new_text.move_to(step_bg)
            return new_text
        
        # ========== SIMPLIFIED SHOP LAYOUT ==========
        # Larger, cleaner zones arranged horizontally
        
        shop_floor = Rectangle(width=13, height=4.5, color="#2a2a3a", 
                               fill_color="#1a1a2a", fill_opacity=0.9, stroke_width=2)
        shop_floor.shift(DOWN * 0.8)
        self.play(FadeIn(shop_floor), run_time=1)
        
        # --- 5 MAIN ZONES (left to right flow) ---
        
        # 1. ENTRANCE
        entrance = RoundedRectangle(width=1.2, height=2.5, corner_radius=0.15, 
                                   color="#4CAF50", fill_color="#4CAF50", fill_opacity=0.25)
        entrance.move_to(LEFT * 5.2 + DOWN * 0.8)
        entrance_label = Text("ENTER", font_size=14, color="#4CAF50", weight=BOLD)
        entrance_label.move_to(entrance)
        
        # 2. QUEUE
        queue = RoundedRectangle(width=2.2, height=2.5, corner_radius=0.15,
                                color="#FF9800", fill_color="#FF9800", fill_opacity=0.2)
        queue.move_to(LEFT * 2.8 + DOWN * 0.8)
        queue_label = Text("QUEUE", font_size=14, color="#FF9800", weight=BOLD)
        queue_label.move_to(queue.get_top() + DOWN * 0.3)
        
        # 3. ORDER / POS
        pos = RoundedRectangle(width=1.8, height=2.5, corner_radius=0.15,
                              color="#2196F3", fill_color="#2196F3", fill_opacity=0.25)
        pos.move_to(LEFT * 0.3 + DOWN * 0.8)
        pos_label = Text("ORDER", font_size=14, color="#2196F3", weight=BOLD)
        pos_label.move_to(pos.get_top() + DOWN * 0.3)
        cash_icon = Text("$", font_size=24, color="#4CAF50")
        cash_icon.move_to(pos.get_center() + DOWN * 0.2)
        
        # 4. BARISTA / MAKE
        barista = RoundedRectangle(width=2.5, height=2.5, corner_radius=0.15,
                                  color="#9C27B0", fill_color="#9C27B0", fill_opacity=0.2)
        barista.move_to(RIGHT * 2.3 + DOWN * 0.8)
        barista_label = Text("BARISTA", font_size=14, color="#9C27B0", weight=BOLD)
        barista_label.move_to(barista.get_top() + DOWN * 0.3)
        coffee_icon = Text("☕", font_size=28)
        coffee_icon.move_to(barista.get_center() + DOWN * 0.2)
        
        # 5. EXIT
        exit_zone = RoundedRectangle(width=1.2, height=2.5, corner_radius=0.15,
                                    color="#F44336", fill_color="#F44336", fill_opacity=0.25)
        exit_zone.move_to(RIGHT * 5.2 + DOWN * 0.8)
        exit_label = Text("EXIT", font_size=14, color="#F44336", weight=BOLD)
        exit_label.move_to(exit_zone)
        
        # Flow arrows between zones
        arrow_style = {"color": WHITE, "stroke_width": 2, "max_tip_length_to_length_ratio": 0.15}
        arrow1 = Arrow(entrance.get_right(), queue.get_left(), buff=0.1, **arrow_style)
        arrow2 = Arrow(queue.get_right(), pos.get_left(), buff=0.1, **arrow_style)
        arrow3 = Arrow(pos.get_right(), barista.get_left(), buff=0.1, **arrow_style)
        arrow4 = Arrow(barista.get_right(), exit_zone.get_left(), buff=0.1, **arrow_style)
        
        shop_elements = VGroup(
            entrance, entrance_label,
            queue, queue_label,
            pos, pos_label, cash_icon,
            barista, barista_label, coffee_icon,
            exit_zone, exit_label,
            arrow1, arrow2, arrow3, arrow4
        )
        
        self.play(FadeIn(shop_elements), run_time=1.5)
        self.wait(1)
        
        # ========== CUSTOMER FLOW ANIMATION ==========
        
        def create_customer():
            return Dot(color="#E91E63", radius=0.2)
        
        # Current step label tracker
        current_step = None
        
        def update_step(text, color="#FFD54F"):
            nonlocal current_step
            new_step = show_step(text, color)
            if current_step:
                self.play(FadeOut(current_step), run_time=0.3)
            self.play(Write(new_step), run_time=0.6)
            current_step = new_step
        
        # --- STEP 1: Customer Arrives ---
        update_step("Step 1: Customer Arrives", "#4CAF50")
        
        customer = create_customer()
        customer.move_to(entrance.get_left() + LEFT * 1)
        self.add(customer)
        
        self.play(customer.animate.move_to(entrance.get_center()), run_time=1.5)
        self.play(Indicate(entrance, color="#4CAF50", scale_factor=1.05), run_time=0.5)
        self.wait(0.5)
        
        # --- STEP 2: Joins Queue ---
        update_step("Step 2: Joins Queue", "#FF9800")
        
        self.play(customer.animate.move_to(queue.get_center()), run_time=1.5)
        self.play(Indicate(queue, color="#FF9800", scale_factor=1.03), run_time=0.5)
        self.wait(0.5)
        
        # --- STEP 3: Places Order (Cash +) ---
        update_step("Step 3: Places Order  (+$)", "#2196F3")
        
        self.play(customer.animate.move_to(pos.get_center() + UP * 0.3), run_time=1.5)
        self.play(
            Flash(cash_icon, color="#4CAF50", line_length=0.3),
            Indicate(pos, color="#2196F3", scale_factor=1.03),
            run_time=0.8
        )
        self.wait(0.5)
        
        # --- STEP 4: Drink Made (Inventory −) ---
        update_step("Step 4: Drink Made  (−Inventory)", "#9C27B0")
        
        self.play(customer.animate.move_to(barista.get_center() + LEFT * 0.5), run_time=1.5)
        self.play(
            Indicate(coffee_icon, color="#FF5722", scale_factor=1.3),
            run_time=1.0
        )
        
        # Coffee appears
        coffee = Dot(color="#8B4513", radius=0.15)
        coffee.move_to(coffee_icon.get_center())
        self.add(coffee)
        self.play(coffee.animate.move_to(customer.get_center()), run_time=0.8)
        self.remove(coffee)
        self.wait(0.3)
        
        # --- STEP 5: Customer Leaves ---
        update_step("Step 5: Customer Leaves!", "#F44336")
        
        self.play(customer.animate.move_to(exit_zone.get_center()), run_time=1.5)
        self.play(Indicate(exit_zone, color="#F44336", scale_factor=1.05), run_time=0.5)
        
        self.play(
            customer.animate.move_to(exit_zone.get_right() + RIGHT * 1),
            FadeOut(customer),
            run_time=1.0
        )
        
        # --- STEP 6: Cycle Repeats ---
        update_step("The Cycle Repeats!", "#FFD54F")
        
        # Quick demo of another customer
        customer2 = create_customer()
        customer2.move_to(entrance.get_left() + LEFT * 1)
        self.add(customer2)
        
        self.play(customer2.animate.move_to(entrance.get_center()), run_time=0.8)
        self.play(customer2.animate.move_to(queue.get_center()), run_time=0.6)
        self.play(customer2.animate.move_to(pos.get_center() + UP * 0.3), run_time=0.6)
        self.play(customer2.animate.move_to(barista.get_center()), run_time=0.6)
        self.play(customer2.animate.move_to(exit_zone.get_center()), run_time=0.6)
        self.play(FadeOut(customer2), run_time=0.4)
        
        # ========== FINAL SUMMARY ==========
        self.wait(0.5)
        
        summary = Text(
            "System Flow: Enter → Queue → Order → Make → Exit",
            font_size=18, color=WHITE
        )
        summary.to_edge(DOWN, buff=0.3)
        
        update_step("Coffee Shop System Complete!", "#4CAF50")
        self.play(Write(summary), run_time=1.0)
        
        self.wait(3)


class StocksFlowsDynamicScene(Scene):
    """
    Clean visualization showing stocks changing dynamically with flows.
    Simplified for clarity.
    """
    
    def construct(self):
        # ========== PHASE INDICATOR (prominent at top) ==========
        phase_bg = Rectangle(width=10, height=0.7, color="#333", 
                            fill_color="#222", fill_opacity=0.95, stroke_width=0)
        phase_bg.to_edge(UP, buff=0.1)
        self.add(phase_bg)
        
        phase_text = Text("Stocks & Flows: Watch the Changes!", font_size=24, color="#FFD54F", weight=BOLD)
        phase_text.move_to(phase_bg)
        self.play(Write(phase_text), run_time=1)
        
        current_phase = phase_text
        
        def update_phase(text, color="#FFD54F"):
            nonlocal current_phase
            new_phase = Text(text, font_size=24, color=color, weight=BOLD)
            new_phase.move_to(phase_bg)
            self.play(FadeOut(current_phase), run_time=0.3)
            self.play(Write(new_phase), run_time=0.6)
            current_phase = new_phase
        
        # ========== STOCK BARS (simple, clean layout) ==========
        stocks = [
            {"name": "Inventory", "color": "#4CAF50", "value": 50},
            {"name": "Orders", "color": "#FF9800", "value": 30},
            {"name": "Cash", "color": "#2196F3", "value": 40},
            {"name": "Customers", "color": "#9C27B0", "value": 60},
        ]
        
        bar_height = 2.8
        bar_width = 1.2
        all_bars = VGroup()
        bar_fills = []
        bar_pcts = []
        
        for i, stock in enumerate(stocks):
            # Container
            container = RoundedRectangle(
                width=bar_width, height=bar_height, corner_radius=0.1,
                color=stock["color"], stroke_width=3, fill_opacity=0.1
            )
            
            # Fill bar
            fill_height = stock["value"] / 100 * (bar_height - 0.2)
            fill = Rectangle(
                width=bar_width - 0.2, height=fill_height,
                fill_color=stock["color"], fill_opacity=0.7, stroke_width=0
            )
            fill.move_to(container.get_bottom() + UP * (fill_height / 2 + 0.1))
            bar_fills.append({"rect": fill, "container": container, "value": stock["value"], "color": stock["color"]})
            
            # Label
            label = Text(stock["name"], font_size=16, color=stock["color"], weight=BOLD)
            label.next_to(container, DOWN, buff=0.15)
            
            # Percentage
            pct = Text(f"{stock['value']}%", font_size=18, color=WHITE, weight=BOLD)
            pct.next_to(container, UP, buff=0.1)
            bar_pcts.append(pct)
            
            group = VGroup(container, fill, label, pct)
            all_bars.add(group)
        
        all_bars.arrange(RIGHT, buff=1.5)
        all_bars.move_to(ORIGIN).shift(DOWN * 0.3)
        
        self.play(FadeIn(all_bars), run_time=1.5)
        self.wait(1)
        
        # ========== FLOW LABELS ==========
        flow_info = VGroup(
            Text("↑ Inflows: Arrivals, Purchases, Orders", font_size=14, color="#4CAF50"),
            Text("↓ Outflows: Departures, Consumption, Fulfillment", font_size=14, color="#F44336"),
        ).arrange(DOWN, buff=0.1)
        flow_info.to_edge(DOWN, buff=0.2)
        self.play(FadeIn(flow_info), run_time=0.8)
        
        # Helper to animate stock changes
        def change_stocks(changes, duration=1.5):
            animations = []
            for i, (delta, new_value) in enumerate(changes):
                if new_value is None:
                    new_value = max(5, min(95, bar_fills[i]["value"] + delta))
                bar_fills[i]["value"] = new_value
                
                container = bar_fills[i]["container"]
                new_height = new_value / 100 * (bar_height - 0.2)
                
                new_fill = Rectangle(
                    width=bar_width - 0.2, height=new_height,
                    fill_color=bar_fills[i]["color"], fill_opacity=0.7, stroke_width=0
                )
                new_fill.move_to(container.get_bottom() + UP * (new_height / 2 + 0.1))
                
                new_pct = Text(f"{new_value}%", font_size=18, color=WHITE, weight=BOLD)
                new_pct.next_to(container, UP, buff=0.1)
                
                animations.append(Transform(bar_fills[i]["rect"], new_fill))
                animations.append(Transform(bar_pcts[i], new_pct))
                
                # Flash effect
                if delta > 0:
                    animations.append(Flash(container, color="#4CAF50", line_length=0.2))
                elif delta < 0:
                    animations.append(Flash(container, color="#F44336", line_length=0.2))
            
            self.play(*animations, run_time=duration)
        
        # ========== PHASE 1: MORNING RUSH ==========
        update_phase("Phase 1: Morning Rush - Customers Flood In!", "#FFD54F")
        self.wait(0.5)
        
        # Customers +30, Orders +40, Inventory -20, Cash +20
        change_stocks([
            (-20, None),  # Inventory down
            (+40, None),  # Orders up
            (+20, None),  # Cash up
            (+30, None),  # Customers up
        ])
        self.wait(0.8)
        
        # ========== PHASE 2: RESTOCKING ==========
        update_phase("Phase 2: Restocking - Supplies Arrive!", "#4CAF50")
        self.wait(0.5)
        
        # Inventory +40, Orders -20, Cash -15
        change_stocks([
            (+40, None),  # Inventory up (restocking)
            (-20, None),  # Orders down (fulfilled)
            (-15, None),  # Cash down (paid supplier)
            (-10, None),  # Customers down slightly
        ])
        self.wait(0.8)
        
        # ========== PHASE 3: AFTERNOON EQUILIBRIUM ==========
        update_phase("Phase 3: Afternoon - System Balances", "#FF9800")
        self.wait(0.5)
        
        # Everything stabilizes
        change_stocks([
            (-10, None),  # Inventory slight down
            (-15, None),  # Orders clearing
            (+10, None),  # Cash up
            (-20, None),  # Customers leaving
        ])
        self.wait(0.8)
        
        # ========== FINAL STATE ==========
        update_phase("System Stabilized!", "#4CAF50")
        
        # Summary
        self.play(FadeOut(flow_info), run_time=0.5)
        summary = VGroup(
            Text("Key Insight:", font_size=20, color=WHITE, weight=BOLD),
            Text("Stocks change through inflows (+) and outflows (−)", font_size=16, color=GRAY),
            Text("Each stock is connected to others in the system!", font_size=16, color=GRAY),
        ).arrange(DOWN, buff=0.1)
        summary.to_edge(DOWN, buff=0.25)
        
        self.play(FadeIn(summary, shift=UP), run_time=1)
        self.wait(3)

